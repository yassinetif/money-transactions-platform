from core.utils.string import convert_partner_cash_to_cash_payload, convert_snake_to_camel_case
from tests.fixtures.api_fixtures import partner_payload, cash_to_cash_base_payload


class TestString:

    def test_convert_partner_cash_to_cash_payload_ok(self, partner_payload, cash_to_cash_base_payload):

        result = convert_partner_cash_to_cash_payload(
            cash_to_cash_base_payload, partner_payload)

        expected_payload = {
            "agent": {
                "code": None
            },
            "amount": "15000",
            "destination_content_object": {
                "address": "DAKAR",
                "first_name": "Felicien",
                "last_name": "Malack",
                "phone_number": "33333333"
            },
            "destination_country": "SN",
            "paid_amount": "15000",
            "source_content_object": {
                "address": "DAKAR",
                "first_name": "Williams",
                "identification_number": None,
                "identification_type": None,
                "issuer_country": None,
                "last_name": "de SOUZA",
                "phone_number": None
            },
            "source_country": "SN",
            "type": None
        }

        assert result == expected_payload

    def test_convert_partner_cash_to_cash_payload_fail(self, partner_payload, cash_to_cash_base_payload):

        result = convert_partner_cash_to_cash_payload(
            cash_to_cash_base_payload, partner_payload)

        expected_payload = {
            "agent": {
                "code": None
            },
            "amount": "15000",
            "destination_content_object": {
                "address": "DAKAR",
                "first_name": "Felicien",
                "last_name": "Malack",
                "phone_number": "XXXX"
            },
            "destination_country": "SN",
            "paid_amount": "15000",
            "source_content_object": {
                "address": "DAKAR",
                "first_name": "Williams",
                "identification_number": None,
                "identification_type": None,
                "issuer_country": None,
                "last_name": "de SOUZA",
                "phone_number": None
            },
            "source_country": "SN",
            "type": None
        }

        assert result != expected_payload

    def test_convert_snake_to_camel_case(self):
        _ = 'ACTIVATION_CARTE'
        result = convert_snake_to_camel_case(_)
        assert result == 'ActivationCarte'
