from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from shared.models import Account, AccountType
from .models import Entity


@receiver(post_save, sender=Entity)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(content_object=instance,
                               category=AccountType.PRINCIPAL, balance=0)
