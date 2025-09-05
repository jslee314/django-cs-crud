from django import forms
from .models import LogUpload

class UploadForm(forms.ModelForm):
    class Meta:
        model = LogUpload
        fields = ['file']
