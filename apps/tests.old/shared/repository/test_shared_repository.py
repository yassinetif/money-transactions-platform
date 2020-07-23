import pytest
from tests.fixtures.shared_fixture import country, corridor, grille_tarifaire, grille_tarifaire_percent
from apps.shared.repository.shared_repository import SharedRepository
from apps.core.errors import CountryException, CorridorException, GrilleException


@pytest.mark.django_db
class TestSharedRepository:

    def test_country_exists(self, country):
        assert country.pk == 1
        assert country.iso == "SN"

    def test_fetch_country_by_iso_success(self, country):
        iso = "SN"
        result = SharedRepository.fetch_country_by_iso(iso)
        assert result == country

    def test_fetch_country_by_iso_raises_exception(self, country):
        iso = "TG"
        with pytest.raises(CountryException) as e:
            SharedRepository.fetch_country_by_iso(iso)
        assert str(e.value) == 'country error'

    def test_fetch_corridor_by_source_and_destination_success(self, corridor):
        transaction_type = "CASH_TO_CASH"
        source_country = "SN"
        destination_country = "SN"
        result = SharedRepository.fetch_corridor_by_source_and_destination(
            transaction_type, source_country, destination_country)
        assert result == corridor

    def test_fetch_corridor_by_source_and_destination_raises_exception(self, country):
        transaction_type = "CASH_TO_CASH"
        source_country = "SN"
        destination_country = "TG"
        with pytest.raises(CorridorException) as e:
            SharedRepository.fetch_corridor_by_source_and_destination(
                transaction_type, source_country, destination_country)
        assert str(e.value) == 'corridor error'

    def test_fetch_grille_by_corridor_success(self, corridor, grille_tarifaire):
        amount = 5000
        result = SharedRepository.fetch_grille_by_corridor(corridor, amount)
        assert result == grille_tarifaire

    def test_fetch_grille_by_corridor_fail(self, corridor):
        amount = 15000
        with pytest.raises(GrilleException) as e:
            SharedRepository.fetch_grille_by_corridor(corridor, amount)
        assert str(e.value) == 'grille error'

    def test_get_fee_by_grille_with_feetype_const_success(self, grille_tarifaire):
        amount = 5000
        result = SharedRepository.get_fee_by_grille(grille_tarifaire, amount)
        assert result == 500

    def test_get_fee_by_grille_with_feetype_percent_success(self, grille_tarifaire_percent):
        amount = 5000
        result = SharedRepository.get_fee_by_grille(grille_tarifaire_percent, amount)
        assert result == 100
    
    def test_fetch_change_parity_value(self):
        # TODO
        pass
