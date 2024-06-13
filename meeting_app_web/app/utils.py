
# utils.py
from .models import *

def find_compatible_users(user):
    user_preferences = CentresDInteret.objects.get(user=user)
    compatible_users = User.objects.filter(
        preferences__interests__in__sport=user_preferences.sport.all(),
        preferences__interests__in__musique=user_preferences.musique.all(),
        preferences__interests__in__lecture=user_preferences.lecture.all(),
        preferences__interests__in__voyage=user_preferences.voyage.all(),
        preferences__interests__in__cinema=user_preferences.cinema.all(),
        preferences__interests__in__technologie=user_preferences.technologie.all()
    ).exclude(id=user.id).distinct()
    
    return compatible_users
