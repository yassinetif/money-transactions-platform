import pytest

@pytest.fixture
def partner_payload():
    return {
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


@pytest.fixture
def cash_to_cash_base_payload():
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
    return base_payload
