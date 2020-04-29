from django.contrib import admin
from entity.models.entity import Entity, EntitySettings
from entity.models.agent import Agent


class EntityAdmin(admin.ModelAdmin):
    list_display = ('code', 'account_number', 'category', 'brand_name', 'country', 'address')


class EntitySettingsAdmin(admin.ModelAdmin):
    list_display = ('entity', 'check_entity_balance', 'overdraft_amount')


class AgentAdmin(admin.ModelAdmin):
    list_display = ('code', 'informations', 'entity', 'phone_number', 'address')


admin.site.register(Entity, EntityAdmin)
admin.site.register(EntitySettings, EntitySettingsAdmin)
admin.site.register(Agent, AgentAdmin)
