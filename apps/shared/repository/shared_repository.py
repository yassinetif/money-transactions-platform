from shared.models import Country, Corridor, Grille, Account, Sharing
from django.db.models import Q
from decimal import Decimal
from core.errors import CorridorException, GrilleException, CountryException


class SharedRepository():

    @staticmethod
    def fetch_country_by_iso(iso: str) -> Country:
        try:
            return Country.objects.get(iso=iso)
        except Country.DoesNotExist as err:
            raise CountryException('country error', err)

    @staticmethod
    def fetch_corridor_by_source_and_destination(transaction_type: str, source_country: str, destination_country: str) -> Corridor:
        try:
            return Corridor.objects.get(
                Q(transaction_type=transaction_type, source_country__iso=source_country,
                  destination_country__iso=destination_country)
                | Q(transaction_type=transaction_type, source_country__iso=source_country, destination_country__isnull=True)
                | Q(transaction_type=transaction_type, source_country__isnull=True, destination_country__iso=destination_country)
                | Q(transaction_type=transaction_type, source_country__isnull=True, destination_country__isnull=True))
        except Corridor.DoesNotExist as err:
            raise CorridorException('corridor error', err)

    @staticmethod
    def fetch_grille_by_corridor(corridor: Corridor, amount: Decimal) -> Grille:
        try:
            return Grille.objects.get(corridor=corridor, maximum_amount__gte=amount, minimum_amount__lte=amount)
        except Grille.DoesNotExist as err:
            raise GrilleException('grille error', err)

    @staticmethod
    def fetch_sharing_calculation_expression(transaction):
        #expression = Sharing.objects.get(corridor=transaction.corridor,ca)
        pass
