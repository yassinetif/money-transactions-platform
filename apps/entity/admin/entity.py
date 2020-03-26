from django.contrib import admin
from entity.models import Entity

class EntityAdmin(admin.ModelAdmin):
    list_display = ('code','category','brand_name','country','address')
    
admin.site.register(Entity, EntityAdmin)