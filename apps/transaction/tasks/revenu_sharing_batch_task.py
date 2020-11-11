from apps.transaction.models import Transaction, RevenuSharingResult
from apps.entity.domain.entity_domain import get_entity_balance, credit_entity
from apps.transaction.domain.transaction_domain import create_batch_transaction, insert_batch_operation


def impact_entity_account_with_commission():
    available_sharings = RevenuSharingResult.objects.filter(is_calculated=False)
    for sharing in available_sharings:
        entity = sharing.entity
        amount = sharing.amount
        entity_last_balance = get_entity_balance(entity)
        credit_entity(entity, entity_last_balance, amount)
        transaction = create_batch_transaction(entity, amount)
        _update_sharing_calculation_status(sharing)
        insert_batch_operation(transaction, entity)

def _update_sharing_calculation_status(sharing):
    sharing.is_calculated = True
    sharing.save()
