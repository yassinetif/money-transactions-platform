from marshmallow import Schema, fields


class AgentValidator(Schema):
    code = fields.Str(required=True)


class SenderCustomerValidator(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    address = fields.Str(required=True)
    identification_type = fields.Str(required=True)
    identification_number = fields.Str(required=True)
    issuer_country = fields.Str(required=True)
    identification_document_deleivery_date = fields.Date(required=True)
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


class CustomerWalletValidator(Schema):
    phone_number = fields.Str(required=True)


class Cash2CashValidator(Schema):
    source_content_object = fields.Nested(
        SenderCustomerValidator(), required=True)
    destination_content_object = fields.Nested(
        ReceiverCustomerValidator(), required=True)
    agent = fields.Nested(AgentValidator(), required=True)
    source_country = fields.Str(required=True)
    destination_country = fields.Str(required=True)
    amount = fields.Str(required=True)
    paid_amount = fields.Decimal(required=True, as_string=True)
    payer_network = fields.Str(required=False, null=True)


class TransactionCash2CashValidator(Schema):
    agent = fields.Nested(AgentValidator(), required=True)
    source_country = fields.Str(required=True)
    destination_country = fields.Str(required=True)
    amount = fields.Str(required=True)
    paid_amount = fields.Decimal(required=True, as_string=True)


class RetraitCashValidator(Schema):
    code = fields.Str(required=True)
    agent = fields.Nested(AgentValidator(), required=True)
    paid_amount = fields.Decimal(required=True, as_string=True)


class SearchTransactionCodeValidator(Schema):
    code = fields.Str(required=True)
    agent = fields.Nested(AgentValidator(), required=True)

class FeeValidator(Schema):
    type = fields.Str(required=True)
    agent = fields.Nested(AgentValidator(), required=True)
    source_country = fields.Str(required=True)
    destination_country = fields.Str(required=True)
    amount = fields.Str(required=True)

class CardActivationValidator(Schema):
    customer = fields.Nested(SenderCustomerValidator(), required=True)
    agent = fields.Nested(AgentValidator(), required=True)
    card_number = fields.Str(required=True)
    paid_amount = fields.Decimal(required=True, as_string=True)
    amount = fields.Str(required=True)

class RechargementCompteEntiteValidator(Schema):
    account_number = fields.Str(required=True)
    agent = fields.Nested(AgentValidator(), required=True)
    paid_amount = fields.Decimal(required=True, as_string=True)
    amount = fields.Str(required=True)


class CashToWalletValidator(Schema):
    source_content_object = fields.Nested(
        SenderCustomerValidator(), required=True)
    destination_content_object = fields.Nested(
        CustomerWalletValidator(), required=True)
    agent = fields.Nested(AgentValidator(), required=True)
    amount = fields.Str(required=True)
    paid_amount = fields.Decimal(required=True, as_string=True)