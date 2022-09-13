from django.contrib import admin

from .models import Portals


class PortalsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'member_id',
        'name',
        'auth_id_create_date',
    )


admin.site.register(Portals, PortalsAdmin)
