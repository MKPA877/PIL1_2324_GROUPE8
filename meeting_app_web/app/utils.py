
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

#Calcul du pourcentage de points communs
def calculate_common_percentage(profile1, profile2):
    preferences = ['sport', 'musique', 'lecture', 'voyage', 'cinema', 'technologie']
    total_preferences = len(preferences)
    common_count = 0

    for pref in preferences:
        if getattr(profile1.pref) == getattr(profile2.pref):
            common_count += 1

    return (common_count / total_preferences) * 100