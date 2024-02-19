from rest_framework import serializers
from .models import Profile, ImageUploader


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'image']  # Add more fields as needed


class ImageUploaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUploader
        fields = ['id', 'image_name', 'image', 'user', 'user_profile', 'date', 'enhanced_image']
