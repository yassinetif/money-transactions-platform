from django.contrib import admin
from transaction.models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Transaction, TransactionAdmin)
