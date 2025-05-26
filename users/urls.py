from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='users'),
    path('/users', views.dashboard, name='users'),
    path('conversation/<int:id>/', views.display_conversation, name='display_conversation'),
]