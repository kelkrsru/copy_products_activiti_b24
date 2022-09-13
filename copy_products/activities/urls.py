from django.urls import path

from . import views

app_name = 'activities'

urlpatterns = [
    path('install/', views.install, name='install'),
    path('uninstall/', views.uninstall, name='uninstall'),
]
