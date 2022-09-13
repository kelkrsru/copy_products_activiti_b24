from django.db import models
from django.utils import timezone
from pybitrix24 import Bitrix24


class Portals(models.Model):
    """Model Portal."""
    member_id = models.CharField(
        verbose_name='Уникальный код портала',
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        verbose_name='Имя портала',
        max_length=255,
    )
    auth_id = models.CharField(
        verbose_name='Токен аутентификации',
        max_length=255,
    )
    auth_id_create_date = models.DateTimeField(
        verbose_name='Дата получения токена аутентификации',
        auto_now=True,
    )
    refresh_id = models.CharField(
        verbose_name='Токен обновления',
        max_length=255,
    )
    client_id = models.CharField(
        verbose_name='Уникальный ID клиента',
        max_length=50,
        null=True,
        blank=True,
    )
    client_secret = models.CharField(
        verbose_name='Секретный токен клиента',
        max_length=100,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Портал'
        verbose_name_plural = 'Порталы'

    def __str__(self):
        return self.name

    def check_auth(self):
        """Method for check auth on portal."""
        if ((self.auth_id_create_date + timezone.timedelta(seconds=3600))
                < timezone.now()):
            bx24 = Bitrix24(self.name)
            # bx24.auth_hostname = 'oauth.bitrix.info'
            bx24._refresh_token = self.refresh_id
            bx24.client_id = self.client_id
            bx24.client_secret = self.client_secret
            bx24.refresh_tokens()
            self.auth_id = bx24._access_token
            self.refresh_id = bx24._refresh_token
