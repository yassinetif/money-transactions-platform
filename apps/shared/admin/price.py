from django.contrib import admin
from shared.models import Corridor, Grille


class GrilleInline(admin.TabularInline):
    model = Grille

class CorridorAdmin(admin.ModelAdmin):
    inlines = [GrilleInline,]


admin.site.register(Corridor, CorridorAdmin)
