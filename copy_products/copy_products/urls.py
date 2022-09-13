from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('settings.urls', namespace='settings')),
    path('install/', include('core.urls', namespace='core')),
    path('activities/', include('activities.urls', namespace='activities')),
    path('admin/', admin.site.urls),
]
