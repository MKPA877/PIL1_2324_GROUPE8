from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
#from django.contrib.auth.forms import  Custom
from django.contrib import messages
from .forms import SignUpForm,LoginForm

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
