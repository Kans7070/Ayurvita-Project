
from unicodedata import name
from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('OTP/', views.otp, name='otp'),
    path('change_password/', views.change_password, name='change_password'),
    path('change_password_OTP/', views.change_password_OTP, name='change_password_OTP'),
    path('profile/', views.profile, name='profile'),
    
    path('edit_profile/<int:id>', views.edit_profile, name='edit_profile'),
    path('change_password_mobile/', views.change_password_mobile,
         name='change_password_mobile'),
         path('resent_register_otp', views.resent_register_otp,
         name='resent_register_otp'),
    path('resent_change_password_otp', views.resent_change_password_otp,
         name='resent_change_password_otp'),
    path('resent_change_password_otp/', views.resent_change_password_otp,
         name='resent_change_password_otp'),
    path('user_logout',views.user_logout, name='user_logout'),
    path('change_password_profile/<int:id>',views.change_password_profile,name='change_password_profile')






]
