from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class SignUpForm(UserCreationForm):
    nom = forms.CharField(max_length=30, required=True)
    prenom = forms.CharField(max_length=30, required=True)
    username = forms.CharField(max_length=30, required=True)
    SEXE_CHOICES = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    )
    sexe = forms.ChoiceField(choices=SEXE_CHOICES, required=True)
    date_naissance = forms.DateField(required=True, help_text='Format: AAAA-MM-JJ')
    lieu_naissance = forms.CharField(max_length=100, required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    email = forms.EmailField(max_length=254, help_text='Requis. Entrez une adresse email valide.', required=True)

    class Meta:
        model = User
        fields = ('username', 'nom', 'prenom', 'sexe', 'date_naissance', 'lieu_naissance', 'bio', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=100)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)



class PreferenceForm(forms.ModelForm):
    class Meta:
        model = CentresDInteret
        fields = ['sport', 'musique', 'voyage', 'technologie', 'lecture', 'cinema']