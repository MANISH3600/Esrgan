# models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

class ImageUploader(models.Model):
    image_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_profile = models.ImageField(default='default.jpg', upload_to='profile_pics')
    date = models.DateField(auto_now_add=True)
    enhanced_image = models.ImageField(upload_to='enhanced_images', blank=True, null=True) 

# Import signals after model definitions
from . import signals
