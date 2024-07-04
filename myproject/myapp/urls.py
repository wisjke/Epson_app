# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_files, name='upload_files'),
    path('process/<int:pk>/', views.process_files, name='process_files'),
]
