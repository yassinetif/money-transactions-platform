from apps.transaction.models import Transaction, TransactionStatus, RevenuSharingResult
from apps.core.errors import TransactionNotFoundException
from datetime import datetime
class TransactionRepository():

    @staticmethod
    def fetch_unpaid_transaction_by_code(code):
        try:
            return Transaction.objects.get(code=code, status=TransactionStatus.PENDING.value)
        except Transaction.DoesNotExist:
            raise TransactionNotFoundException(
                'unavailable transaction code', 'Transaction code  : {0} not found or already paid'.format(code))

    @staticmethod
    def save_entity_commission(transaction, entity, amount):
        RevenuSharingResult.objects.create(transaction=transaction,
                                           entity=entity, amount=amount)

    @staticmethod
    def retreive_transaction_by_number(number):
        try:
            return Transaction.objects.get(number=number)
        except Transaction.DoesNotExist:
            raise TransactionNotFoundException(
                'unavailable transaction code', 'Transaction code  : {0} not found or already paid'.format(number))

    @staticmethod
    def fetch_revenu_sharing_results(entity):
        try:
            return RevenuSharingResult.objects.filter(entity=entity, created=datetime.today())
        except Transaction.DoesNotExist:
            return None
