from django.conf import settings
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from settings.models import SettingsPortal

from .models import Portals


@xframe_options_exempt
@csrf_exempt
def install(request):
    """Method install application."""
    try:
        portal: Portals = Portals.objects.get(
            member_id=request.POST['member_id'])
        portal.auth_id = request.POST['AUTH_ID']
        portal.refresh_id = request.POST['REFRESH_ID']
        portal.save()
    except Portals.DoesNotExist:
        portal: Portals = Portals.objects.create(
            member_id=request.POST['member_id'],
            name=request.GET.get('DOMAIN'),
            auth_id=request.POST['AUTH_ID'],
            refresh_id=request.POST['REFRESH_ID']
        )
    try:
        SettingsPortal.objects.get(portal=portal)
    except SettingsPortal.DoesNotExist:
        SettingsPortal.objects.create(portal=portal)

    return render(request, 'core/install.html',
                  {'app_name': settings.APP_NAME})
