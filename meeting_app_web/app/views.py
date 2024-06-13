from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.contrib import messages
from .forms import *
from .models import *
from .utils import *
from .models import UserProfile, Friendship



def index_view(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('accueil')  # Redirection après connexion
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect. Peut être que vous n'avez pas de compte")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # Authentifier l'utilisateur après inscription
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('accueil')  # Rediriger l'utilisateur vers la page d'accueil après inscription
    else:
        form = SignUpForm()
    return render(request, 'inscription.html', {'form': form})


#@login_required
def preference_view(request):
    if request.method == 'POST':
        form = PreferenceForm(request.POST, instance=request.user.preference)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vos préférances ont été enregistrées avec succès!')
            return redirect('preferences')
    else:
        form = PreferenceForm(instance=request.user.preference)
    return render(request, 'preferences.html', {'form': form})


@login_required
def compatible_profiles(request):
    user = request.user
    compatible_users = find_compatible_users(user)
    return render(request, 'compatible_profils.html', {'compatible_users': compatible_users})

# Vues pour les suggestions d'amis en fonction du sexe opposé
def suggestions_view(request):
    user_profile = request.user.userprofile
    
    #récupération de tous les profils d'utilisateurs de sexe opposé
    opposite_profiles = UserProfile.objects.exclude(user=request.user), filter(user__gender='opposé')

    suggestions = []

    for profile in opposite_profiles:
        common_percentage = calculate_common_percentage(user_profile, profile)
        suggestions.append((profile, common_percentage))

    # Triage des suggestions par pourcentage de points communs(ordre décroissant)
    suggestions = sorted(suggestions, key=lambda x: x[1], reverse=True)

    return render(request, 'suggestions.html', {'suggestions': suggestions})

