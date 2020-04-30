from django.db.models.signals import post_save
from django.dispatch import receiver
from shared.models.account import Account, AccountType
from kyc.models import Customer


@receiver(post_save, sender=Customer)
def create_customer_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(content_object=instance,
                               category=AccountType.PRINCIPAL, balance=0)
