from django.contrib import admin
from apps.entity.models.entity import Entity, EntitySettings, EntityForm
from apps.entity.models.agent import Agent, AgentForm


class EntityAdmin(admin.ModelAdmin):
    form = EntityForm
    list_display = ('image_tag', 'code', 'account_number', 'category', 'brand_name', 'country', 'address')

    def image_tag(self, obj):
        from django.utils.html import escape
        return u'<img src="%s" />' % escape(obj.logo.url)
    image_tag.short_description = 'Logo'
    image_tag.allow_tags = True


class EntitySettingsAdmin(admin.ModelAdmin):
    list_display = ('entity', 'check_entity_balance', 'overdraft_amount')


class AgentAdmin(admin.ModelAdmin):
    form = AgentForm
    list_display = ('code', 'informations', 'entity', 'phone_number', 'address')


admin.site.register(Entity, EntityAdmin)
admin.site.register(EntitySettings, EntitySettingsAdmin)
admin.site.register(Agent, AgentAdmin)
