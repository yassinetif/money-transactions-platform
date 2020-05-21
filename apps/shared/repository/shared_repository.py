from apps.shared.models.country import Country, Change
from apps.shared.models.price import Corridor, Grille, FeeType, AGENT_TRANSACTIONS, Sharing
from django.db.models import Q
from apps.core.errors import CorridorException, GrilleException, CountryException, CoreException
from apps.shared.models.account import Account, AccountType


class SharedRepository():

    @staticmethod
    def fetch_country_by_iso(iso):
        try:
            return Country.objects.get(iso=iso)
        except Country.DoesNotExist as err:
            raise CountryException('XXX error', err)

    def fetch_currency_by_country_iso(iso):
        try:
            return SharedRepository.fetch_country_by_iso(iso).currency.iso
        except Country.DoesNotExist as err:
            raise CountryException('country currency error', err)

    @staticmethod
    def fetch_corridor_by_source_and_destination(transaction_type, source_country, destination_country):
        try:
            return Corridor.objects.get(Q(transaction_type=transaction_type, source_country__iso=source_country,
                                          destination_country__iso=destination_country) | Q(transaction_type=transaction_type, source_country__iso=source_country,
                                                                                            destination_country__isnull=True) | Q(transaction_type=transaction_type, source_country__isnull=True,
                                                                                                                                  destination_country__iso=destination_country) | Q(
                                                                                                                                      transaction_type=transaction_type, source_country__isnull=True,
                destination_country__isnull=True))
        except Corridor.DoesNotExist as err:
            raise CorridorException('No corridor is found for this transaction type', err)

    @staticmethod
    def fetch_grille_by_corridor(corridor, amount):
        try:
            return Grille.objects.get(corridor=corridor, maximum_amount__gte=amount, minimum_amount__lte=amount)
        except Grille.DoesNotExist as err:
            raise GrilleException('grille error', err)

    @staticmethod
    def get_fee_by_grille(grille, amount):
        if grille.fee_type == FeeType.CONST.value:
            return grille.fee
        else:
            return amount * grille.fee / 100

    @staticmethod
    def fetch_change_parity_value(source_currency, destination_currency):
        try:
            change = Change.objects.get(source_currency__iso=source_currency, destination_currency__iso=destination_currency, status=True)
            return change.parity
        except Change.DoesNotExist as err:
            raise CoreException('unable to find change for currencies', err)

    @staticmethod
    def fetch_sharing_calculation_expression(transaction):
        corridor = transaction.grille.corridor
        result = None
        if transaction.transaction_type in AGENT_TRANSACTIONS:
            try:
                sharing = Sharing.objects.get(corridor=corridor, calculation_expression__contains=transaction.agent.entity.brand_name)
            except Sharing.DoesNotExist:
                sharing = Sharing.objects.get(corridor=corridor, is_standard=True)
            result = sharing.calculation_expression
        return result

    @staticmethod
    def initialize_account(instance, created, is_card_activation):
        if created:
            Account.objects.create(content_object=instance,
                                   category=AccountType.PRINCIPAL.value, balance=0)
            if is_card_activation:
                Account.objects.create(content_object=instance,
                                       category=AccountType.CARTE_MONNAMON.value, balance=0)
