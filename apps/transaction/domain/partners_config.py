WORLD_REMIT = {
    'entity' : 'WORLD REMIT'
    'test': {
        'url': 'https://payoutapi.worldremit.com/v1/payout/transactions/',
        'credentials': {
            'headers': {'Content-type': 'application/json; charset=utf-8',
                        'Authorization': 'Basic EAAAANANYpY3541qOuuHfA991vQZ0NCA8mqpqfYMyZsCYOg5og8hThnp4zrEDqbXtCVNnYs+Dw3ED'
                        'XhM3Um16jBFkXFbBdkgBeqU0P2U0XoJmkMFhi/lk197DtgnLRucrXv5CQ==',
                        'Authorization-Token': 'C9156AAD714C4FDFA2F5E68D1100B4F8'
                        }
        }
    },
    'production': {
        'url': 'https://payoutapi.worldremit.com/v1/payout/transactions/',
        'credentials': {
            'headers': {'Content-type': 'application/json; charset=utf-8',
                        'Authorization': 'Basic EAAAANANYpY3541qOuuHfA991vQZ0NCA8mqpqfYMyZsCYOg5og8hThnp4zrEDqbXtCVNnYs+Dw3ED'
                        'XhM3Um16jBFkXFbBdkgBeqU0P2U0XoJmkMFhi/lk197DtgnLRucrXv5CQ==',
                        'Authorization-Token': 'C9156AAD714C4FDFA2F5E68D1100B4F8'
                        }
        }
    }
    'payload':
        {'source_content_object': {'first_name': 'sender_first_name',
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
         'paid_amount': 'payout_amount'},

    'transaction_id': 'wr_transaction_id',
    'transaction_number': 'wr_transaction_number'
}
