from django.db import models
from enum import Enum
from django.utils.translation import ugettext_lazy as _


class NotificationType(Enum):
    SMS = 'SMS'
    EMAIL = 'EMAIL'


class Notification(models.Model):
    notification_type = models.CharField(max_length=30, choices=[
        (tag.value, tag.value) for tag in NotificationType], default=NotificationType.SMS.value)
    content = models.TextField(max_length=500)
    content_receiver = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.notification_type)

    class Meta:
        verbose_name = _('Notifications Log')
