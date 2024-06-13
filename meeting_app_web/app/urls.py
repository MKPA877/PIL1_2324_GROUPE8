from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('inscription/', signup_view, name='inscription'),
    path('preferences/', preference_view, name='preferences'),
    path('compatible-profils/', compatible_profiles, name='compatible_profils'),
]