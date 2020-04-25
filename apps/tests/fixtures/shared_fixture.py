import pytest
from shared.models import Country, Corridor, Grille, FeeType


@pytest.fixture
def country():
    country = Country(**{
        'iso': 'SN'
    })
    country.save()
    return country


@pytest.fixture
def corridor(country):
    return Corridor.objects.create(
        transaction_type='CASH_TO_CASH', source_country=country,
        destination_country=country)

@pytest.fixture
def grille_tarifaire(corridor):
    fee_type = FeeType.CONST.value
    return Grille.objects.create(corridor=corridor,
                                 maximum_amount=10000,
                                 minimum_amount=0, fee_type=fee_type,
                                 fee=500)

@pytest.fixture
def grille_tarifaire_percent(corridor):
    fee_type = FeeType.PERCENT.value
    return Grille.objects.create(corridor=corridor,
                                 maximum_amount=10000,
                                 minimum_amount=0, fee_type=fee_type,
                                 fee=2)
