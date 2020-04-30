from django.apps import AppConfig
import logging
logger = logging.getLogger(__name__)


class CustomerConfig(AppConfig):
    name = 'kyc'
    verbose_name = "Customer"
    verbose_name_plural = "Customers"

    def ready(self):
        from kyc import signals
        logger.info(signals)
