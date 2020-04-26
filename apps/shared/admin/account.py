from django.contrib import admin
from shared.models.account import Account
from django.utils.translation import ugettext_lazy as _


class AccountAdmin(admin.ModelAdmin):

    list_display = ('account_object_type', 'balance', 'created')

    def account_object_type(self, obj):
        return obj.content_object
    account_object_type.allow_tags = True
    account_object_type.short_description = _('Entités / Clients')


admin.site.register(Account, AccountAdmin)
