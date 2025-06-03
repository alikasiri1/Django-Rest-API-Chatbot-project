from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, ChatView,
    PageListView, PageDetailView
)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Page management endpoints
    path('pages/', PageListView.as_view(), name='page-list'),
    path('pages/<uuid:pk>/', PageDetailView.as_view(), name='page-detail'),
    
    # Chat endpoints
    path('chat/', ChatView.as_view(), name='chat'),
    # path('chat/history/', ChatHistoryView.as_view(), name='chat_history'),
]