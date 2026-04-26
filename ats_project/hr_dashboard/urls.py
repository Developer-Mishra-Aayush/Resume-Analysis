from django.urls import path
from . import views

app_name = 'hr_dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('candidate_detail/', views.candidate_detail, name='candidate_detail'),
    path('job_descriptions/', views.job_descriptions, name='job_descriptions'),
    path('analytics/', views.analytics, name='analytics'),
    path('create_new_job/', views.create_new_job, name='create_new_job'),
]