import pytest
from shared.models import Country


@pytest.fixture
@pytest.mark.django_db
def country():
    country = Country(**{
        'iso': 'SN'
    })
    country.save()
    return country
