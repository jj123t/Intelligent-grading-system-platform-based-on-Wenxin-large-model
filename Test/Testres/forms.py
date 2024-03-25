from django import forms
from .models import ImageUpload


class FileUploadForm(forms.Form):
    file = forms.FileField()
    user_info = forms.CharField(max_length=255)

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']