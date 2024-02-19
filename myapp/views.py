from models.realesrgan_model import RealESRGANModel
from models.realesrnet_model import RealESRNetModel




from .forms import UserRegsitrationForm, UpdateUserForm, ProfileUpdateForm, ImageUploadForm
from .models import ImageUploader,User
from .utils import enhance_image  # Assuming you have a utility function to enhance images
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageUploaderSerializer




class ImageUploadAPIView(APIView):
    def post(self, request, format=None):
        serializer = ImageUploaderSerializer(data=request.data)
        if serializer.is_valid():
            img_uploader = serializer.save(
                user=request.user,
                user_profile=request.user.profile.image.url,
                date=datetime.now()
            )

            # Enhance the uploaded image using ESRGAN
            enhanced_img = enhance_image(img_uploader.image)

            # Save the enhanced image to the database
            img_uploader.enhanced_image = enhanced_img
            img_uploader.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageDeleteAPIView(APIView):
    def delete(self, request, image_id, format=None):
        image = get_object_or_404(ImageUploader, pk=image_id)

        if image.user == request.user:
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You are not authorized to delete this image."}, status=status.HTTP_403_FORBIDDEN)

















@login_required
def home(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid.")  # Debug print statement
            img_name = form.cleaned_data['image_name']
            img = form.cleaned_data['image']
            u_profile = request.user.profile.image.url

            # Save the original image to the database
            img_uploader = ImageUploader.objects.create(
                image_name=img_name,
                image=img,
                user=request.user,
                user_profile=u_profile,
                date=datetime.now()
            )

            # Enhance the uploaded image using ESRGAN
            enhanced_img = enhance_image(img)  # Implement this function to use ESRGAN model

            # Save the enhanced image to the database
            img_uploader.enhanced_image = enhanced_img
            img_uploader.save()

            messages.success(request, 'Your Image Uploaded and Enhanced Successfully !!')
            return redirect('home')
        else:
            print("Form is not valid:", form.errors)  # Debug print statement
    else:
        form = ImageUploadForm()

    images = ImageUploader.objects.filter(user=request.user)
    return render(request, 'home.html', {'form': form, 'images': images})


def signup(request):
        if request.method == "POST":
                fm = UserRegsitrationForm(request.POST)
                if fm.is_valid():
                        fm.save()
                        messages.success(request,'Signup Done !!')

        else:
                fm  = UserRegsitrationForm()

        context = {'fm':fm}
        return render(request,'signup.html',context)

@login_required
def profile(request):

        if request.method == "POST":
                u_form = UpdateUserForm(instance = request.user,data=request.POST)
                p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
                if u_form.is_valid() and p_form.is_valid():
                    u_form.save()
                    p_form.save()
                    messages.success(request, f'Your Profile has been updated!')


        
        
        else:
                u_form = UpdateUserForm(instance = request.user)
                p_form = ProfileUpdateForm(instance = request.user.profile)

        return render(request,'profile.html',{'u_form':u_form,'p_form':p_form})


def user_profile(request,user):

        users = User.objects.get(username=user)
        image = ImageUploader.objects.filter(user=user)


        return render(request,'user-profile.html',{'users':users,'image':image})
@login_required
def delete_image(request, image_id):
    # Get the image object from the database
    image = get_object_or_404(ImageUploader, pk=image_id)

    # Check if the user is the owner of the image
    if image.user == request.user:
        # Delete the image
        image.delete()
        messages.success(request, 'Image deleted successfully!')
    else:
        messages.error(request, 'You are not authorized to delete this image.')

    # Redirect back to the home page
    return redirect('home')