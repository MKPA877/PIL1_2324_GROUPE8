from django.db.models import Q
from .models import User, CentresDInteret

def find_compatible_users(user):
    try:
        user_preferences = CentresDInteret.objects.get(user=user)
    except CentresDInteret.DoesNotExist:
        # Gérer le cas où l'utilisateur n'a pas de préférences définies
        return User.objects.none()

    compatible_users = User.objects.filter(
        Q(centres_d_interet__sport=user_preferences.sport) |
        Q(centres_d_interet__musique=user_preferences.musique) |
        Q(centres_d_interet__lecture=user_preferences.lecture) |
        Q(centres_d_interet__voyage=user_preferences.voyage) |
        Q(centres_d_interet__cinema=user_preferences.cinema) |
        Q(centres_d_interet__technologie=user_preferences.technologie)
    ).exclude(id=user.id).distinct()

    for compatible_user in compatible_users:
        compatible_user.common_percentage = calculate_common_percentage(user_preferences, compatible_user.centres_d_interet)

    return compatible_users

# Calcul du pourcentage de points communs
def calculate_common_percentage(profile1, profile2):
    preferences = ['sport', 'musique', 'lecture', 'voyage', 'cinema', 'technologie']
    total_preferences = len(preferences)
    common_count = 0

    for pref in preferences:
        if getattr(profile1, pref) == getattr(profile2, pref):
            common_count += 1

    return (common_count / total_preferences) * 100
