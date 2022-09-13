from core.models import Portals
from django.db import models


class SettingsPortal(models.Model):
    """Model for settings portal."""
    portal = models.OneToOneField(
        Portals,
        verbose_name='Портал',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Настройка портала'
        verbose_name_plural = 'Настройки портала'

        ordering = ['portal', 'pk']

    def __str__(self):
        return 'Настройки для портала {}'.format(self.portal.name)
