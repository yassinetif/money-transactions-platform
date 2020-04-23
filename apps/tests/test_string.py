import pytest
from core.utils import convert_partner_cash_to_cash_payload


class TestString:

    def test_convert_partner_cash_to_cash_payload_ok(self):

        partner_payload = {
            'wr_transaction_id': '11111111',
            'wr_transaction_number': '22222222',
            'originating_country': 'SN',
            'destination_country': 'SN',
            'sending_amount': '15000',
            'payout_amount': '15000',
            'sender_first_name': 'Williams',
            'sender_last_name': 'de SOUZA',
            'sender_city': 'DAKAR',
            'receiver_first_name': 'Felicien',
            'receiver_last_name': 'Malack',
            'receiver_city': 'DAKAR',
            'receiver_mobile_number': '33333333',
        }

        base_payload = {'source_content_object': {'first_name': 'sender_first_name',
                                                  'last_name': 'sender_last_name',
                                                  'phone_number': '773453810',
                                                  'address': 'sender_city',
                                                  'identification_number': 'EB012412312',
                                                  'identification_type': 'PP',
                                                  'issuer_country': 'TG'},
                        'destination_content_object': {'first_name': 'receiver_first_name',
                                                       'last_name': 'receiver_last_name',
                                                       'phone_number': 'receiver_mobile_number',
                                                       'address': 'receiver_city'},
                        'type': 'CASH_TO_CASH',
                        'agent': {'code': '086796'},
                        'source_country': 'originating_country',
                        'destination_country': 'destination_country',
                        'amount': 'payout_amount',
                        'paid_amount': 'payout_amount'}
        result = convert_partner_cash_to_cash_payload(
            base_payload, partner_payload)

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
