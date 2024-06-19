from django.urls import path
from .views import *

urlpatterns = [
    path('', index_view, name='index'),
    path('login/', login_view, name='login'),
    path('inscription/', signup_view, name='inscription'),
    path('preferences/', preference_view, name='preferences'),
    path('compatible-profils/', compatible_profiles, name='compatible_profils'),
    path('chat/<str:chat_id>/', chat_room, name='chatroom'),
    path('chat/<int:user_id>/', private_chat_redirect, name='private_chat_redirect'),
]