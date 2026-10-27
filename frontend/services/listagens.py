import os
from typing import Any

import requests
import streamlit as st


XANO_LISTAGENS_ENABLED_ENV = "XANO_LISTAGENS_ENABLED"
XANO_PACIENTES_URL_ENV = "XANO_PACIENTES_URL"
XANO_PROFISSIONAIS_URL_ENV = "XANO_PROFISSIONAIS_URL"
REQUEST_TIMEOUT_SECONDS = 5


class ListagemError(Exception):
    """Erro esperado ao carregar uma listagem do Xano."""


class IntegracaoDesabilitadaError(ListagemError):
    """Indica que a integração ainda não foi explicitamente habilitada."""


class ConfiguracaoAusenteError(ListagemError):
    """Indica que a URL necessária não foi configurada."""


class ErroHttpError(ListagemError):
    """Indica uma resposta HTTP de erro."""


class ErroTransporteError(ListagemError):
    """Indica timeout ou falha de conexão."""


class RespostaInvalidaError(ListagemError):
    """Indica JSON ou estrutura de resposta incompatível."""


def integracao_habilitada() -> bool:
    return os.getenv(XANO_LISTAGENS_ENABLED_ENV, "").strip().lower() == "true"


@st.cache_data(ttl=60, show_spinner=False)
def _listar_pacientes_cacheado(url: str | None) -> list[dict[str, Any]]:
    return _buscar_colecao(url, XANO_PACIENTES_URL_ENV, ("id", "nome", "telefone", "email"))


@st.cache_data(ttl=60, show_spinner=False)
def _listar_profissionais_cacheado(url: str | None) -> list[dict[str, Any]]:
    return _buscar_colecao(
        url, XANO_PROFISSIONAIS_URL_ENV, ("id", "nome", "telefone", "email", "especialidade")
    )


def listar_pacientes(url: str | None) -> list[dict[str, Any]]:
    _exigir_integracao_habilitada()
    return _listar_pacientes_cacheado(url)


def listar_profissionais(url: str | None) -> list[dict[str, Any]]:
    _exigir_integracao_habilitada()
    return _listar_profissionais_cacheado(url)


def invalidar_cache_pacientes() -> None:
    _listar_pacientes_cacheado.clear()


def invalidar_cache_profissionais() -> None:
    _listar_profissionais_cacheado.clear()


def _exigir_integracao_habilitada() -> None:
    if not integracao_habilitada():
        raise IntegracaoDesabilitadaError(
            "A integração com o Xano está desabilitada por segurança."
        )


def _buscar_colecao(
    url: str | None,
    nome_configuracao: str,
    campos: tuple[str, ...],
) -> list[dict[str, Any]]:
    if not url or not url.strip():
        raise ConfiguracaoAusenteError(
            f"A configuração {nome_configuracao} não foi definida."
        )

    try:
        resposta = requests.get(url.strip(), timeout=REQUEST_TIMEOUT_SECONDS)
    except requests.Timeout as erro:
        raise ErroTransporteError("A consulta ao Xano excedeu o tempo limite.") from erro
    except requests.ConnectionError as erro:
        raise ErroTransporteError("Não foi possível conectar ao Xano.") from erro
    except requests.RequestException as erro:
        raise ErroTransporteError("Falha ao consultar o Xano.") from erro

    if not resposta.ok:
        raise ErroHttpError(f"O Xano respondeu com erro HTTP {resposta.status_code}.")

    try:
        dados = resposta.json()
    except ValueError as erro:
        raise RespostaInvalidaError("O Xano retornou um JSON inválido.") from erro

    if not isinstance(dados, list):
        raise RespostaInvalidaError("A resposta do Xano não é uma lista.")

    registros: list[dict[str, Any]] = []
    for indice, item in enumerate(dados):
        if not isinstance(item, dict) or any(campo not in item for campo in campos):
            raise RespostaInvalidaError(
                f"O registro {indice + 1} não contém os campos esperados."
            )
        registros.append({campo: item[campo] for campo in campos})

    return registros
