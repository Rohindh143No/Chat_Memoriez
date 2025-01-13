from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat_view'),  # Default chat view
    path('chat/download_chat/<str:participant>/', views.download_chat, name='download_chat'),  # Download chat
    path('chat/view_chat/<str:participant>/', views.view_chat, name='view_chat'),  # View specific chat
    path('howto/', views.howto_view, name='howto'),
    path('files/', views.chat_file_list, name='chat_file_list'),  # Route to render elif.html
]
