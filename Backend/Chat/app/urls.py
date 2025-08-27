from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import UserView,ChatView,MessageView,RegistrationView

routers = DefaultRouter()
routers.register(r'chat',ChatView,basename='chat')
routers.register(r'message',MessageView,basename='message')
routers.register(r'user',UserView,basename='user')

urlpatterns = [
    path('',include(routers.urls)),
    path('register/',RegistrationView.as_view(),name='register'),
    
]
