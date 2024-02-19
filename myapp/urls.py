from django.urls import path
from .import views
from django.contrib.auth import views as authviews

urlpatterns = [
    path('',views.home,name="home"),
    path("signup/", views.signup, name="signup"),
    path('login/',authviews.LoginView.as_view(template_name="login.html")),
    path('logout/',authviews.LogoutView.as_view(template_name="logout.html")),
    path('profile/',views.profile,name="profile"),
    path('profile/<str:user>/',views.user_profile,name="user_profile"),
    path('delete/<int:image_id>/', views.delete_image, name='delete_image'),

    path('api/image_upload/', views.ImageUploadAPIView.as_view(), name='image_upload'),
    path('api/image_delete/<int:image_id>/', views.ImageDeleteAPIView.as_view(), name='image_delete'),

]


