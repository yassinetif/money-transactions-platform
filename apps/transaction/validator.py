from marshmallow import Schema, fields


class AgentValidator(Schema):
    code = fields.Str(required=True)


class CustomerValidator(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    address = fields.Str(required=True)
    identification_type = fields.Str(required=True)
    identification_number = fields.Str(required=True)
    issuer_country = fields.Str(required=True)


class Cash2CashValidator(Schema):
    source_content_object = fields.Nested(CustomerValidator(), required=True)
    destination_content_object = fields.Nested(CustomerValidator(), required=True)
    agent = fields.Nested(AgentValidator(), required=True)
    source_country = fields.Str(required=True)
    destination_country = fields.Str(required=True)
    amount = fields.Str(required=True)
    paid_amount = fields.Decimal(required=True,as_string=True)


class SearchTransactionCodeValidator(Schema):
    code = fields.Str(required=True)
    agent = fields.Nested(AgentValidator(), required=True)
