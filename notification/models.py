from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Add new notification types TO THE END of the list
NOTIFICATION_TYPES = (
)


class Notification(models.Model):
    type = models.CharField(verbose_name=_('Model Notification Field type'), max_length=2, choices=NOTIFICATION_TYPES)
    user = models.ForeignKey('auth.User', verbose_name=_('Model Notification Field user'), related_name='notifications', on_delete=models.CASCADE)
    notified_by = models.ForeignKey('auth.User', verbose_name=_('Model Notification Field notified_by'), null=True, blank=True, on_delete=models.CASCADE, related_name='notifications_made')
    message = models.CharField(verbose_name=_('Model Notification Field message'), max_length=200)
    is_read = models.BooleanField(verbose_name=_('Model Notification Field is_read'), default=False)
    created_at = models.DateTimeField(verbose_name=_('Model Notification Field created_at'), null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.now()

        super(Notification, self).save(*args, **kwargs)
