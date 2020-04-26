from django.db.models.signals import post_save
from django.dispatch import receiver
from shared.models.account import Account, AccountType
from entity.models.entity import Entity


@receiver(post_save, sender=Entity)
def create_entity_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(content_object=instance,
                               category=AccountType.PRINCIPAL, balance=0)
