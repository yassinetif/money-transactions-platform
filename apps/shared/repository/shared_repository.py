from shared.models.country import Country
from shared.models.price import Corridor, Grille, FeeType
from django.db.models import Q
from core.errors import CorridorException, GrilleException, CountryException


class SharedRepository():

    @staticmethod
    def fetch_country_by_iso(iso):
        try:
            return Country.objects.get(iso=iso)
        except Country.DoesNotExist as err:
            raise CountryException('country error', err)

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
            raise CorridorException('corridor error', err)

    @staticmethod
    def fetch_grille_by_corridor(corridor, amount):
        try:
            return Grille.objects.get(corridor=corridor, maximum_amount__gte=amount, minimum_amount__lte=amount)
        except Grille.DoesNotExist as err:
            raise GrilleException('grille error', err)

    @staticmethod
    def calculate_fee_by_grille(grille, amount):
        if grille.fee_type == FeeType.CONST.value:
            return grille.fee
        else:
            return amount * grille.fee / 100

    @staticmethod
    def fetch_sharing_calculation_expression(transaction):
        # TODO : get right calculation expression for revenu sharing
        pass
