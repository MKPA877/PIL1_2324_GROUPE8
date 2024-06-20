from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', index_view, name='index'),
    path('login/', login_view, name='login'),
    path('inscription/', signup_view, name='inscription'),
    path('preferences/', preference_view, name='preferences'),
    path('compatible-profils/', compatible_profiles, name='compatible_profils'),
    path('chat/room/<int:chat_id>/', chat_room, name='chat_room'),
    path('upload-profile-picture/', upload_profile_picture, name='upload_profile_picture'),
    path('send_invitation/<str:to_username>/', send_invitation, name='send_invitation'),
    path('accept_invitation/<int:connection_id>/', accept_invitation, name='accept_invitation'),
    path('notifications/', notification_list, name='notification_list'),
    path('upload_profile_picture/', upload_profile_picture, name='upload_profile_picture'),
    path('change_username/', change_username, name='change_username'),
    path('change_bio/', change_bio, name='change_bio'),
    path('gest_profil/', go_to_gest_profil, name='gest_profil'),
    path('conversations/', conversations_view, name='conversations_view'),
    path('private_chat/<str:username>/', private_chat_redirect, name='private_chat_redirect'),
    path('ws/room/<int:chat_id>/', chat_room, name='chat_room'),
    path('logout/', conversations_view, name='logout')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)