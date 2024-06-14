from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.contrib import messages
from .forms import *
from .models import *
from .utils import *



def index_view(request):
    if request.method == 'POST' and 'Continuer' in request.POST:
        return redirect('login')  # Redirection vers la page de connexion
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
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('accueil')  # Rediriger l'utilisateur vers la page d'accueil après inscription
    else:
        form = SignUpForm()
    return render(request, 'inscription.html', {'form': form})


@login_required
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


@login_required
def conversations_view(request):
    user = request.user
    connections = Connection.objects.filter(
        (Q(sender=user) | Q(receiver=user)) & Q(accepted=True)
    ).distinct()

    context = []
    for connection in connections:
        last_message = connection.messages.order_by('-date_envoi').first()
        other_participant = connection.receiver if connection.sender == user else connection.sender
        context.append({
            'connection': connection,
            'last_message': last_message,
            'other_participant': other_participant,
        })
    return render(request, 'conversations.html', {'conversations': context})


def suggestions_view(request):
    user_profile = request.user.userprofile
    
    # Récupération de tous les profils d'utilisateurs de sexe opposé
    opposite_profiles = User.objects.exclude(id=request.user.id).filter(gender='F' if user_profile.gender == 'M' else 'M')
    
    suggestions = []

    for profile in opposite_profiles:
        common_percentage = calculate_common_percentage(user_profile, profile.userprofile)
        suggestions.append((profile, common_percentage))

    # Triage des suggestions par pourcentage de points communs (ordre décroissant)
    suggestions = sorted(suggestions, key=lambda x: x[1], reverse=True)

    return render(request, 'suggestions.html', {'suggestions': suggestions})


@login_required
def private_chat_redirect(request, user_id):
    user1 = request.user
    user2 = get_object_or_404(User, id=user_id)
    
    if user1 == user2:
        return redirect('some_error_page')  # Rediriger vers une page d'erreur ou gérer le cas
    
    # Vérifiez si une connexion existe déjà entre ces utilisateurs
    connection = Connection.objects.filter(
        (Q(sender=user1) & Q(receiver=user2)) | (Q(sender=user2) & Q(receiver=user1))
    ).first()
    
    if not connection:
        connection = Connection.objects.create(sender=user1, receiver=user2, accepted=True)
    
    chat = PrivateChat.objects.filter(connection=connection).first()
    if not chat:
        chat = PrivateChat.objects.create(connection=connection)
    
    return redirect('chat_room', chat_id=chat.id)


@login_required
def chat_room(request, chat_id):
    chat = get_object_or_404(PrivateChat, id=chat_id)
    return render(request, 'chat_room.html', {'chat_id': chat.id})
