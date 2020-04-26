from django.contrib import admin
from shared.models import Corridor, Grille, Sharing


class GrilleInline(admin.TabularInline):
    model = Sharing


class SharingInline(admin.TabularInline):
    model = Grille


class CorridorAdmin(admin.ModelAdmin):
    inlines = [GrilleInline, SharingInline]
    list_display = ('name', 'source_country', 'destination_country', 'created')


admin.site.register(Corridor, CorridorAdmin)
