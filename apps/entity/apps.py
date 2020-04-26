from django.apps import AppConfig
import logging
logger = logging.getLogger(__name__)


class EntityConfig(AppConfig):
    name = 'entity'
    verbose_name = "Partner"
    verbose_name_plural = "Partners"

    def ready(self):
        from entity import signals
        logger.info(signals)
