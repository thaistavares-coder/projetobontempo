import os
import unittest
from unittest.mock import Mock, patch

import requests

from services.xano import (
    DEFAULT_PACIENTES_BASE_URL,
    DEFAULT_PROFISSIONAIS_BASE_URL,
    REQUEST_TIMEOUT_SECONDS,
    XANO_API_ENABLED_ENV,
    XANO_PACIENTES_BASE_URL_ENV,
    XANO_PROFISSIONAIS_BASE_URL_ENV,
    ResourceEndpoints,
    XanoClient,
    XanoConfigurationError,
    XanoConnectionError,
    XanoHTTPError,
    XanoResponseError,
    XanoSettings,
    XanoTimeoutError,
    XanoTransportError,
    api_enabled,
)


class TestXanoClient(unittest.TestCase):
    def setUp(self) -> None:
        self.transport = Mock()
        self.settings = XanoSettings(
            patients_base_url="https://patients.example.invalid/api:patients",
            professionals_base_url=(
                "https://professionals.example.invalid/api:professionals"
            ),
            patients=ResourceEndpoints(
                collection_path="pacientes",
                item_path="paciente/{paciente_id}",
                create_path="pacientes",
                update_path="paciente/{paciente_id}",
                delete_path="paciente/{paciente_id}",
                identifier_parameter="paciente_id",
            ),
            professionals=ResourceEndpoints(
                collection_path="profissionais",
                item_path="profissional/{profissional_id}",
                create_path="profissionais",
                update_path="profissional/{profissional_id}",
                delete_path="profissional/{profissional_id}",
                identifier_parameter="profissional_id",
            ),
        )
        self.client = XanoClient(self.settings, self.transport)
        self.patient = {
            "id": 11,
            "nome": "Paciente sintético",
            "telefone": "11999999999",
            "email": "patient@example.invalid",
            "extra": "não expor",
        }
        self.professional = {
            "id": 21,
            "nome": "Profissional sintético",
            "telefone": "11888888888",
            "email": None,
            "especialidade": "Especialidade textual",
        }

    def _response(self, data: object, status_code: int = 200) -> Mock:
        response = Mock()
        response.status_code = status_code
        response.json.return_value = data
        return response

    def test_reads_collection_and_individual_records_with_resource_ids(self) -> None:
        self.transport.request.side_effect = [
            self._response([self.patient]),
            self._response(self.patient),
            self._response([self.professional]),
            self._response(self.professional),
        ]

        patient_list = self.client.list_records("pacientes")
        patient = self.client.get_record("pacientes", 11)
        professional_list = self.client.list_records("profissionais")
        professional = self.client.get_record("profissionais", 21)

        self.assertEqual(patient_list, [{key: value for key, value in self.patient.items() if key != "extra"}])
        self.assertEqual(patient, patient_list[0])
        self.assertEqual(professional_list, [self.professional])
        self.assertEqual(professional, self.professional)
        urls = [call.args[1] for call in self.transport.request.call_args_list]
        self.assertEqual(
            urls,
            [
                "https://patients.example.invalid/api:patients/pacientes",
                "https://patients.example.invalid/api:patients/paciente/11",
                "https://professionals.example.invalid/api:professionals/profissionais",
                "https://professionals.example.invalid/api:professionals/profissional/21",
            ],
        )
        self.assertTrue(
            all(
                call.kwargs["timeout"] == REQUEST_TIMEOUT_SECONDS
                for call in self.transport.request.call_args_list
            )
        )

    def test_creates_and_updates_both_resources_with_trimmed_text_fields(self) -> None:
        self.transport.request.side_effect = [
            self._response(self.patient),
            self._response(self.professional),
            self._response(self.patient),
            self._response(self.professional),
        ]

        self.client.create_record(
            "pacientes",
            {
                "nome": " Paciente sintético ",
                "telefone": " 11999999999 ",
                "email": " patient@example.invalid ",
            },
        )
        self.client.create_record(
            "profissionais",
            {
                "nome": " Profissional sintético ",
                "telefone": " 11888888888 ",
                "email": "",
                "especialidade": " Clínica ",
            },
        )
        self.client.update_record("pacientes", 11, {"email": None})
        self.client.update_record(
            "profissionais",
            21,
            {"especialidade": "Clínica geral"},
        )

        calls = self.transport.request.call_args_list
        self.assertEqual(
            [call.args[0] for call in calls],
            ["POST", "POST", "PATCH", "PATCH"],
        )
        self.assertEqual(
            calls[0].kwargs["json"],
            {
                "nome": "Paciente sintético",
                "telefone": "11999999999",
                "email": "patient@example.invalid",
            },
        )
        self.assertEqual(
            calls[1].kwargs["json"],
            {
                "nome": "Profissional sintético",
                "telefone": "11888888888",
                "email": "",
                "especialidade": "Clínica",
            },
        )
        self.assertEqual(calls[2].kwargs["json"], {"email": None})
        self.assertEqual(
            calls[3].kwargs["json"], {"especialidade": "Clínica geral"}
        )

    def test_delete_requires_confirmed_success_response(self) -> None:
        self.transport.request.return_value = self._response({"success": True})

        self.client.delete_record("pacientes", 11)
        self.client.delete_record("profissionais", 21)

        self.assertEqual(
            [call.args[1] for call in self.transport.request.call_args_list],
            [
                "https://patients.example.invalid/api:patients/paciente/11",
                "https://professionals.example.invalid/api:professionals/profissional/21",
            ],
        )
        for invalid_response in ({}, {"success": False}, {"success": "true"}, []):
            with self.subTest(invalid_response=invalid_response):
                self.transport.request.return_value = self._response(invalid_response)
                with self.assertRaises(XanoResponseError):
                    self.client.delete_record("pacientes", 11)

    def test_http_errors_preserve_status_without_exposing_response_body(self) -> None:
        for status_code in (400, 401, 403, 404, 409, 500):
            with self.subTest(status_code=status_code):
                self.transport.request.return_value = self._response(
                    {"private": "do not expose"}, status_code
                )
                with self.assertRaises(XanoHTTPError) as raised:
                    self.client.list_records("pacientes")
                self.assertEqual(raised.exception.status_code, status_code)
                self.assertNotIn("private", str(raised.exception))

    def test_transport_failures_are_explicit(self) -> None:
        cases = (
            (requests.Timeout, XanoTimeoutError),
            (requests.ConnectionError, XanoConnectionError),
            (requests.RequestException, XanoTransportError),
        )
        for error_type, expected in cases:
            with self.subTest(error_type=error_type):
                self.transport.request.side_effect = error_type("synthetic")
                with self.assertRaises(expected):
                    self.client.list_records("pacientes")

    def test_invalid_json_shapes_fields_and_ids_are_rejected(self) -> None:
        invalid_json = self._response(None)
        invalid_json.json.side_effect = ValueError("invalid")
        self.transport.request.return_value = invalid_json
        with self.assertRaises(XanoResponseError):
            self.client.list_records("pacientes")

        for invalid in (
            {"id": 1},
            [{"id": 1}],
            [{**self.patient, "id": True}],
            [{**self.patient, "email": 12}],
        ):
            with self.subTest(invalid=invalid):
                self.transport.request.return_value = self._response(invalid)
                with self.assertRaises(XanoResponseError):
                    self.client.list_records("pacientes")

        with self.assertRaises(ValueError):
            self.client.get_record("pacientes", True)
        with self.assertRaises(ValueError):
            self.client.delete_record("pacientes", 0)

    def test_invalid_payloads_do_not_send_request(self) -> None:
        with self.assertRaises(XanoResponseError):
            self.client.create_record("pacientes", {"nome": " "})
        with self.assertRaises(XanoResponseError):
            self.client.create_record("pacientes", {"nome": "Nome", "id": 99})
        self.transport.request.assert_not_called()

    def test_default_routes_and_base_urls_match_confirmed_contract(self) -> None:
        settings = XanoSettings.from_environment()
        self.assertEqual(settings.patients_base_url, DEFAULT_PACIENTES_BASE_URL)
        self.assertEqual(
            settings.professionals_base_url, DEFAULT_PROFISSIONAIS_BASE_URL
        )
        self.assertEqual(settings.patients.item_path, "paciente/{paciente_id}")
        self.assertEqual(
            settings.professionals.item_path,
            "profissional/{profissional_id}",
        )
        self.transport.request.return_value = self._response({"success": True})
        XanoClient(settings, self.transport).delete_record("profissionais", 21)
        self.assertEqual(
            self.transport.request.call_args.args[1],
            f"{DEFAULT_PROFISSIONAIS_BASE_URL}/profissional/21",
        )

    def test_urls_can_be_overridden_externally_and_missing_values_fail_closed(self) -> None:
        with patch.dict(
            os.environ,
            {
                XANO_PACIENTES_BASE_URL_ENV: "",
                XANO_PROFISSIONAIS_BASE_URL_ENV: (
                    "https://custom.example.invalid/api:custom"
                ),
            },
            clear=True,
        ):
            settings = XanoSettings.from_environment()
            client = XanoClient(settings, self.transport)
            with self.assertRaises(XanoConfigurationError):
                client.list_records("pacientes")
            self.transport.request.return_value = self._response([])
            self.assertEqual(client.list_records("profissionais"), [])

        self.assertEqual(
            self.transport.request.call_args.args[1],
            "https://custom.example.invalid/api:custom/profissionais",
        )
        self.assertEqual(settings.patients_base_url, "")

    def test_api_is_disabled_unless_explicitly_enabled(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(api_enabled())
        with patch.dict(os.environ, {XANO_API_ENABLED_ENV: "false"}, clear=True):
            self.assertFalse(api_enabled())
        with patch.dict(os.environ, {XANO_API_ENABLED_ENV: "true"}, clear=True):
            self.assertTrue(api_enabled())


if __name__ == "__main__":
    unittest.main()
