from django.contrib import admin
from django.urls import path,include
from .views import login_view,signup_view, verify_otp, resend_otp

app_name = 'accounts'

urlpatterns = [
    path('',signup_view,name='signup_view'),
    path('login/',login_view,name='login_view'),
    path('verification/',verify_otp,name='verify_otp'),
    path('resend-otp/', resend_otp, name='resend_otp'),
]
