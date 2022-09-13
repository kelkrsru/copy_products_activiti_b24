from core.models import Portals
from django.db import models


class SettingsPortal(models.Model):
    """Модель настроек для портала."""
    id_smart_process_cargo = models.PositiveSmallIntegerField(
        verbose_name='ID smart процесса "Груз"',
        default=0,
    )
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
