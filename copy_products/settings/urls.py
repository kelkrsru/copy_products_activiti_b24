from django.urls import path
from settings import views

app_name = 'settings'

urlpatterns = [
    path('', views.index, name='index')
]
