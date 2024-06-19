from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class SignUpForm(UserCreationForm):
    nom = forms.CharField(max_length=30, required=True)
    prenom = forms.CharField(max_length=30, required=True)
    sexe = forms.ChoiceField(choices=User.gender_choices, required=True)
    date_naissance = forms.DateField(required=True, help_text='Format: AAAA-MM-JJ')
    lieu_naissance = forms.CharField(max_length=100, required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    email = forms.EmailField(max_length=254, help_text='Requis. Entrez une adresse email valide.', required=True)

    class Meta:
        model = User
        fields = ('username', 'nom', 'prenom', 'sexe', 'date_naissance', 'lieu_naissance', 'bio', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data['nom']
        user.last_name = self.cleaned_data['prenom']
        user.gender = self.cleaned_data['sexe']
        user.date_of_birth = self.cleaned_data['date_naissance']
        user.place_of_birth = self.cleaned_data['lieu_naissance']
        user.bio = self.cleaned_data['bio']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=100)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)



class PreferenceForm(forms.ModelForm):
    class Meta:
        model = CentresDInteret
        fields = ['sport', 'musique', 'voyage', 'technologie', 'lecture', 'cinema']