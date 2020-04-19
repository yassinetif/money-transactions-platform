from transaction.models import Transaction, TransactionStatus
from core.errors import TransactionNotFoundException


class TransactionRepository():

    @staticmethod
    def fetch_unpaid_transaction_by_code(code: str) -> Transaction:
        try:
            return Transaction.objects.get(code=code, status=TransactionStatus.PENDING.value)
        except Transaction.DoesNotExist as err:
            raise TransactionNotFoundException(
                str(err), 'No transaction is found')
