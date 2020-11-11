from apps.transaction.models import Transaction, RevenuSharingResult
from apps.entity.domain.entity_domain import get_entity_balance, credit_entity
from apps.transaction.domain.transaction_domain import create_batch_transaction


def impact_entity_account_with_commission():
    available_sharings = RevenuSharingResult.objects.filter(is_calculated=False)
    for sharing in available_sharings:
        entity = sharing.entity
        amount = sharing.amount
        entity_last_balance = get_entity_balance(entity)
        print (entity)
        print (entity_last_balance)
        print (amount)
        #credit_entity(entity, entity_last_balance, amount)
        create_batch_transaction(amount, entity)
