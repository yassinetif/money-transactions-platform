from django.contrib import admin
from entity.models.entity import Entity

class EntityAdmin(admin.ModelAdmin):
    list_display = ('code', 'account_number', 'category', 'brand_name', 'country', 'address')


admin.site.register(Entity, EntityAdmin)
