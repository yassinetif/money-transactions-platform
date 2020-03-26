from django.apps import AppConfig


class EntityConfig(AppConfig):
    name = 'entity'
    verbose_name = "Partner"
    verbose_name_plural = "Partners"

    def ready(self):
        import entity.signals
