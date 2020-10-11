from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.core.utils.string import random_code
from django import forms
from django.contrib.auth.models import User
from apps.entity.models.entity import Entity
from enum import Enum


class AgentHabilitation(Enum):
    AGENT = 'AGENT'
    SUPERVISEUR = 'SUPERVISEUR'
    ADMIINISTRATEUR = 'ADMIINISTRATEUR'
    AGENT_FINANCE = 'AGENT_FINANCE'
   


class AuthenticationType(Enum):
    DEFAULT = 'DEFAULT'
    OTP = 'OTP'

class Agent(models.Model):
    habilitation = models.CharField(max_length=30, choices=[
        (tag.value, tag.value) for tag in AgentHabilitation],default=AgentHabilitation.AGENT.value)

    code = models.CharField(
        unique=True,
        max_length=10,
        null=False,
        blank=False,
        default=random_code(6),
    )
    informations = models.OneToOneField(User, on_delete=models.CASCADE)
    entity = models.ForeignKey(Entity, on_delete=models.DO_NOTHING, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    authentication_type = models.CharField(max_length=30, choices=[
        (tag.value, tag.value) for tag in AuthenticationType], default='DEFAULT')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.informations.username

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.code = random_code(6)
        super(Agent, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Agent")
        verbose_name_plural = _("Agents")
        app_label = 'entity'

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        exclude = ('code',)
