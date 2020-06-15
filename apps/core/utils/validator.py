from marshmallow import Schema, fields


class AgentValidator(Schema):
    code = fields.Str(required=True)


class CreationWalletValidator(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=False, null=True)
    phone_number = fields.Str(required=True)
    address = fields.Str(required=True)
    identification_type = fields.Str(required=True)
    identification_number = fields.Str(required=True)
    issuer_country = fields.Str(required=True)
    identification_document_delivery_date = fields.Date(required=True)
    identification_document_expiry_date = fields.Date(required=True)
    country = fields.Str(required=False)


class ReceiverCustomerValidator(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    address = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    identification_type = fields.Str(required=False)
    identification_number = fields.Str(required=False)
    issuer_country = fields.Str(required=False)
    country = fields.Str(required=False)


class CustomerWalletValidator(Schema):
    phone_number = fields.Str(required=True)


class WalletBalanceValidator(Schema):
    phone_number = fields.Str(required=True)

class CashToCashValidator(Schema):
    source_content_object = fields.Nested(
        CreationWalletValidator(), required=True)
    destination_content_object = fields.Nested(
        ReceiverCustomerValidator(), required=True)
    source_country = fields.Str(required=True)
    destination_country = fields.Str(required=True)
    amount = fields.Str(required=True)
    payer_network = fields.Str(required=False, null=True)
    motif_envoi = fields.Str(required=True)
    source_revenu = fields.Str(required=True)


class RetraitCashValidator(Schema):
    code = fields.Str(required=True)
    paid_amount = fields.Decimal(required=True, as_string=True)
    destination_content_object = fields.Nested(
        CreationWalletValidator(), required=True)

class SearchTransactionCodeValidator(Schema):
    code = fields.Str(required=True)

class FeeValidator(Schema):
    type = fields.Str(required=True)
    source_country = fields.Str(required=True)
    destination_country = fields.Str(required=True)
    amount = fields.Str(required=True)

class ActivationCarteValidator(Schema):
    customer = fields.Nested(CreationWalletValidator(), required=True)
    card_number = fields.Str(required=True)
    amount = fields.Str(required=True)

class CreditCompteEntiteValidator(Schema):
    account_number = fields.Str(required=True)
    amount = fields.Str(required=True)


class DebitCompteEntiteValidator(CreditCompteEntiteValidator):
    pass


class CashToWalletValidator(Schema):
    source_content_object = fields.Nested(
        CreationWalletValidator(), required=True)
    destination_content_object = fields.Nested(
        CustomerWalletValidator(), required=True)
    amount = fields.Str(required=True)

class WalletToCashValidator(Schema):
    destination_content_object = fields.Nested(
        ReceiverCustomerValidator(), required=True)
    amount = fields.Str(required=True)

class WalletToWalletValidator(Schema):
    destination_content_object = fields.Nested(
        CustomerWalletValidator(), required=True)
    amount = fields.Str(required=True)


class WalletLoginValidator(Schema):
    phone_number = fields.Str(required=True)
    password = fields.Str(required=True)
