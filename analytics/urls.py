from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('user/<str:user_id>/', views.user_detail, name='user_detail'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('testuser/', views.testuser, name='testuser'),
] 