from django.urls import path
from . import views

app_name = 'candidate_dashboard'

urlpatterns = [
    # path('', views.home, name='home'),
    # path('logout/', views.logout_view, name='logout')
    path('', views.candidate_dashboard, name='candidate_dashboard'),
    path('upload/',views.upload, name='upload'),
    path('my_resumes/', views.my_resumes, name='my_resumes'),
    path('last_result/', views.last_result, name='last_result'),
    path('chat_with_resume/', views.chat_with_resume, name='chat_with_resume')
]