from django.contrib import admin
from entity.models import Agent


class AgentAdmin(admin.ModelAdmin):
    list_display = ('code', 'informations', 'entity',
                    'phone_number', 'address')


admin.site.register(Agent, AgentAdmin)
