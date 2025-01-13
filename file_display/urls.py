# file_display/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('display/', views.display_chat_file_list, name='display_chat_file_list'),  # List files
    path('display/<str:filename>/', views.display_file, name='display_chat_file'),  # View individual file
]
