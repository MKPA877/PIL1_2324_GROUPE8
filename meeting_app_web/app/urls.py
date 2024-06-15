from django.urls import path
from .views import *

urlpatterns = [
    path('', index_view, name='index'),
    #path('login/', login_view, name='login'),
    #path('inscription/', signup_view, name='inscription'),
    path('preferences/', preference_view, name='preferences'),
    #path('compatible-profils/', compatible_profiles, name='compatible_profils'),
    path('upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path('profile/', views.profile, name='profile'), 
    path('change-username/', views.change_username, name='change_username'),
    path('/change_bio/', views.change_bio, name='change_bio'),
    path('messaging/', views.messaging, name='messaging'),
]