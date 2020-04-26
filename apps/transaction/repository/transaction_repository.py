from transaction.models import Transaction, TransactionStatus
from core.errors import TransactionNotFoundException


class TransactionRepository():

    @staticmethod
    def fetch_unpaid_transaction_by_code(code):
        try:
            return Transaction.objects.get(code=code, status=TransactionStatus.PENDING.value)
        except Transaction.DoesNotExist:
            raise TransactionNotFoundException(
                'unavailable transaction code', {'reponse_code': 'ERR', 'response_text': 'unavailable transaction code'})
