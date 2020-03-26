from django.db import models
from django.contrib.auth.models import User
from .entity import Entity


class Agent(models.Model):
    informations = models.OneToOneField(User, on_delete=models.CASCADE)
    entity = models.OneToOneField(Entity, on_delete=models.DO_NOTHING)
    phone_number = models.CharField(max_length=10, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.informations.username

    class Meta:
        verbose_name = "Agent"
        verbose_name_plural = "Agents"
