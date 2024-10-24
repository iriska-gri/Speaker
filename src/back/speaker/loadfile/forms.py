from django import forms

from .models import *


class UploadCallsForm(forms.ModelForm):
    class Meta:
        model = UploadCalls
        fields = '__all__'