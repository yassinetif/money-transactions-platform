from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
import logging
logger = logging.getLogger(__name__)


class EntityConfig(AppConfig):
    name = 'entity'
    verbose_name = _("Partner")
    verbose_name_plural = _("Partners")

    def ready(self):
        from entity import signals
        logger.info(signals)
