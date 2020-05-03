from shared.models.price import Corridor, Grille, Sharing
from shared.models.country import Country, Currency, Change
from django.contrib import admin
from shared.models.account import Account
from django.utils.translation import ugettext_lazy as _


class AccountAdmin(admin.ModelAdmin):

    list_display = ('account_object_type', 'category', 'balance', 'created')

    def account_object_type(self, obj):
        return obj.content_object
    account_object_type.allow_tags = True
    account_object_type.short_description = _('Entités / Clients')


admin.site.register(Account, AccountAdmin)


class CountryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Country, CountryAdmin)


class GrilleInline(admin.TabularInline):
    model = Sharing


class SharingInline(admin.TabularInline):
    model = Grille


class CorridorAdmin(admin.ModelAdmin):
    inlines = [GrilleInline, SharingInline]
    list_display = ('name', 'transaction_type', 'source_country', 'destination_country', 'currency', 'created')
    save_as = True


admin.site.register(Corridor, CorridorAdmin)


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso', 'status', 'created')


admin.site.register(Currency, CurrencyAdmin)


class ChangeAdmin(admin.ModelAdmin):
    list_display = ('name', 'source_currency', 'destination_currency', 'status')


admin.site.register(Change, ChangeAdmin)
