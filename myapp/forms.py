from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

from .models import ImageUploader


class UserRegsitrationForm(UserCreationForm):

        class Meta:
                model = User
                fields = ['username']

class UpdateUserForm(forms.ModelForm):

        email = forms.EmailField()
        class Meta:
                model = User
                fields = ['username','email','first_name','last_name']
                
class ProfileUpdateForm(forms.ModelForm):
            class Meta:
                model = Profile
                fields = ['image']





class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUploader
        fields = ['image_name', 'image']