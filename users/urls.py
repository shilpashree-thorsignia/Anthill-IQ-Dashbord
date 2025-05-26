from django.urls import path
from . import views
from.views import chat_history

urlpatterns = [
    path('', views.login, name='users'),
    path('/users', views.dashboard, name='users'),
    path('chat-history/<str:id>/', chat_history, name='chat_history'),
]