from transaction.models import Transaction
from core.errors import TransactionNotFoundException


class TransactionRepository():

    @staticmethod
    def fetch_transaction_by_code(code: str) -> Transaction:
        try:
            return Transaction.objects.get(code=code)
        except Transaction.DoesNotExist as err:
            raise TransactionNotFoundException('No transaction is found', str(err))
