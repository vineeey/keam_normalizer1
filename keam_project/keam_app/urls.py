# keam_app/urls.py
from django.urls import path
from . import views

app_name = 'keam_app'  # App namespace

urlpatterns = [
    path('', views.intro, name='intro'),
    path('select-year/', views.select_year, name='select_year'),
    path('marks-form/', views.marks_form, name='marks_form'),
    path('result/', views.result, name='result'),
    path('upload/', views.upload_and_process, name='upload'),
    path('api/webhook/', views.webhook_listener, name='webhook'),  # Added for API integration
]