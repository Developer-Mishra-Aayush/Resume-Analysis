from django.contrib import admin
from django.urls import path,include
from .views import login_view,signup_view,verification_view

urlpatterns = [
    path('',signup_view,name='signup_view'),
    path('login/',login_view,name='login_view'),
    path('verification/',verification_view,name='verification_view')
]
