import unittest
from unittest.mock import Mock, patch

import requests

from services import listagens


class TestListagens(unittest.TestCase):
    def setUp(self) -> None:
        self.ambiente = patch.dict(
            "os.environ", {listagens.XANO_LISTAGENS_ENABLED_ENV: "true"}
        )
        self.ambiente.start()
        self.addCleanup(self.ambiente.stop)
        listagens.invalidar_cache_pacientes()
        listagens.invalidar_cache_profissionais()
        self.url_pacientes = "https://example.invalid/pacientes"
        self.url_profissionais = "https://example.invalid/profissionais"
        self.registro_paciente = {
            "id": 1,
            "nome": "Paciente de teste",
            "telefone": "000000000",
            "email": "teste@example.invalid",
            "campo_interno": "não deve ser exibido",
        }
        self.registro_profissional = {
            "id": 2,
            "nome": "Médico de teste",
            "telefone": "000000001",
            "email": "medico@example.invalid",
            "especialidade": "Clínica de teste",
        }

    def tearDown(self) -> None:
        listagens.invalidar_cache_pacientes()
        listagens.invalidar_cache_profissionais()

    def _resposta(self, dados: object, status_code: int = 200) -> Mock:
        resposta = Mock()
        resposta.ok = status_code < 400
        resposta.status_code = status_code
        resposta.json.return_value = dados
        return resposta

    @patch("services.listagens.requests.get")
    def test_lista_pacientes_somente_com_campos_previstos(self, get: Mock) -> None:
        get.return_value = self._resposta([self.registro_paciente])

        resultado = listagens.listar_pacientes(self.url_pacientes)

        self.assertEqual(
            resultado,
            [
                {
                    "id": 1,
                    "nome": "Paciente de teste",
                    "telefone": "000000000",
                    "email": "teste@example.invalid",
                }
            ],
        )
        get.assert_called_once_with(
            self.url_pacientes, timeout=listagens.REQUEST_TIMEOUT_SECONDS
        )

    @patch("services.listagens.requests.get")
    def test_lista_profissionais_preserva_especialidade_textual(self, get: Mock) -> None:
        get.return_value = self._resposta([self.registro_profissional])

        resultado = listagens.listar_profissionais(self.url_profissionais)

        self.assertEqual(resultado[0]["especialidade"], "Clínica de teste")
        get.assert_called_once_with(
            self.url_profissionais, timeout=listagens.REQUEST_TIMEOUT_SECONDS
        )

    @patch("services.listagens.requests.get")
    def test_lista_vazia_eh_sucesso(self, get: Mock) -> None:
        get.return_value = self._resposta([])

        self.assertEqual(listagens.listar_pacientes(self.url_pacientes), [])

    @patch("services.listagens.requests.get")
    def test_integracao_desabilitada_nao_faz_requisicao(self, get: Mock) -> None:
        with patch.dict("os.environ", {listagens.XANO_LISTAGENS_ENABLED_ENV: "false"}):
            with self.assertRaises(listagens.IntegracaoDesabilitadaError):
                listagens.listar_pacientes(self.url_pacientes)

        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(listagens.IntegracaoDesabilitadaError):
                listagens.listar_pacientes(self.url_pacientes)

        get.assert_not_called()

    @patch("services.listagens.requests.get")
    def test_configuracao_ausente_nao_faz_requisicao(self, get: Mock) -> None:
        with self.assertRaisesRegex(
            listagens.ConfiguracaoAusenteError, listagens.XANO_PACIENTES_URL_ENV
        ):
            listagens.listar_pacientes(None)

        get.assert_not_called()

    @patch("services.listagens.requests.get")
    def test_erro_http_nao_vira_lista_vazia(self, get: Mock) -> None:
        get.return_value = self._resposta({"erro": "simulado"}, status_code=503)

        with self.assertRaises(listagens.ErroHttpError):
            listagens.listar_pacientes(self.url_pacientes)

    @patch("services.listagens.requests.get")
    def test_timeout_e_falha_de_conexao(self, get: Mock) -> None:
        get.side_effect = requests.Timeout
        with self.assertRaises(listagens.ErroTransporteError):
            listagens.listar_pacientes(self.url_pacientes)

        listagens.invalidar_cache_pacientes()
        get.side_effect = requests.ConnectionError
        with self.assertRaises(listagens.ErroTransporteError):
            listagens.listar_pacientes(self.url_pacientes)

    @patch("services.listagens.requests.get")
    def test_json_invalido_e_estrutura_incompativel(self, get: Mock) -> None:
        resposta = self._resposta(None)
        resposta.json.side_effect = ValueError("JSON inválido simulado")
        get.return_value = resposta
        with self.assertRaises(listagens.RespostaInvalidaError):
            listagens.listar_pacientes(self.url_pacientes)

        listagens.invalidar_cache_pacientes()
        get.return_value = self._resposta({"id": 1})
        with self.assertRaises(listagens.RespostaInvalidaError):
            listagens.listar_pacientes(self.url_pacientes)

    @patch("services.listagens.requests.get")
    def test_registro_com_campos_incompativeis(self, get: Mock) -> None:
        get.return_value = self._resposta([{"id": 1, "nome": "Incompleto"}])

        with self.assertRaises(listagens.RespostaInvalidaError):
            listagens.listar_pacientes(self.url_pacientes)

    @patch("services.listagens.requests.get")
    def test_cache_reutiliza_resultado_e_refresh_invalida_somente_seu_modulo(
        self, get: Mock
    ) -> None:
        get.side_effect = [
            self._resposta([self.registro_paciente]),
            self._resposta([self.registro_profissional]),
            self._resposta([]),
        ]

        listagens.listar_pacientes(self.url_pacientes)
        listagens.listar_pacientes(self.url_pacientes)
        listagens.listar_profissionais(self.url_profissionais)
        self.assertEqual(get.call_count, 2)

        listagens.invalidar_cache_pacientes()
        listagens.listar_pacientes(self.url_pacientes)
        listagens.listar_profissionais(self.url_profissionais)
        self.assertEqual(get.call_count, 3)


if __name__ == "__main__":
    unittest.main()
