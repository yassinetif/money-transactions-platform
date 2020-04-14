from django.contrib import admin
from shared.models import Corridor, Grille, Sharing
from django.utils.translation import ugettext_lazy as _


class GrilleInline(admin.TabularInline):
    model = Sharing


class SharingInline(admin.TabularInline):
    model = Grille


class CorridorAdmin(admin.ModelAdmin):
    inlines = [GrilleInline, SharingInline]
    list_display = ('name', 'source_country', 'destination_country', 'created')


admin.site.register(Corridor, CorridorAdmin)
