from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.shared.models.account import Account, AccountType
from apps.kyc.models import Customer


@receiver(post_save, sender=Customer)
def create_customer_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(content_object=instance,
                               category=AccountType.PRINCIPAL.value, balance=0)
