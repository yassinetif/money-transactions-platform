from apps.shared.models.price import Corridor, Grille, Sharing, MotifEnvoi, SourceRevenu
from apps.shared.models.country import Country, Currency, Change
from apps.shared.models.notification import Notification
from django.contrib import admin
from apps.shared.models.account import Account
from django.utils.translation import ugettext_lazy as _

class AccountAdmin(admin.ModelAdmin):

    list_display = ('account_object_type', 'category', 'account_object_currency', 'created')

    def account_object_type(self, obj):
        return obj.content_object
    account_object_type.allow_tags = True
    account_object_type.short_description = _('Entités / Clients')

    def account_object_currency(self, obj):
        if obj.content_object.country:
            return '{0} {1}'.format(obj.balance, obj.content_object.country.currency.iso)
    account_object_currency.allow_tags = True
    account_object_currency.short_description = 'Devise'

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


admin.site.register(Account, AccountAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('iso', 'code', 'status')

    def code(self, obj):
        return obj.iso.code
    code.allow_tags = True
    code.short_description = _('Code')


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


class NotificationAdmin(admin.ModelAdmin):
    search_fields = ('content_receiver',)
    list_display = ('notification_type', 'content', 'content_receiver', 'created', 'status')


admin.site.register(Notification, NotificationAdmin)

class MotifEnvoiAdmin(admin.ModelAdmin):
    list_display = ('code', 'libelle')


admin.site.register(MotifEnvoi, MotifEnvoiAdmin)


class SourceRevenuAdmin(admin.ModelAdmin):
    list_display = ('code', 'libelle')


admin.site.register(SourceRevenu, SourceRevenuAdmin)
