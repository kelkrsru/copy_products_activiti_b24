from django import forms

from .models import SettingsPortal


class SettingsPortalForm(forms.ModelForm):
    """Form for Settings portal."""
    class Meta:
        model = SettingsPortal
        fields = '__all__'
        exclude = ('portal',)
