from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.contrib import messages
from .forms import *
from .models import *
from .utils import *
from .forms import ProfilePictureForm



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


@login_required 
def upload_profile_picture(request):
    if request.methode == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form= ProfilePictureForm(instance=request.user)
    return render(request, 'upload_profile_picture.html', {'form': form})

@login_required 
def change_username(request):
    if request.methode == 'POST':
        form = UsernameChangeForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.sucess(request, 'Your username has been updated successfully!')
            return redirect('profile')
        else:
            form = UsernameChangeForm(instance=request.user)
        return render(request, 'change_username.html', {'form': form}) 

@login_required 
def change_username(request):
    if request.methode == 'POST':
        form = BioChangeForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.sucess(request, 'Your bio has been updated successfully!')
            return redirect('profile')
        else:
            form = BioChangeForm(instance=request.user)
        return render(request, 'change_bio.html', {'form': form}) 


@login_required 
def messaging(request):
    return render(request, 'messagin.html')
