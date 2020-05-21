from apps.transaction.models import Transaction, TransactionStatus
from apps.core.errors import TransactionNotFoundException


class TransactionRepository():

    @staticmethod
    def fetch_unpaid_transaction_by_code(code):
        try:
            return Transaction.objects.get(code=code, status=TransactionStatus.PENDING.value)
        except Transaction.DoesNotExist:
            raise TransactionNotFoundException(
                'unavailable transaction code', 'Transaction code  : {0} not found or already paid'.format(code))
