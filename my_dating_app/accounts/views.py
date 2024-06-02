from my_dating_app import settings
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from .token import generatorToken
def home(request):
    return render(request, 'app/index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if User.objects.filter(username=username):
            messages.error(request, "Ce nom d'utilisateur est déjà pris")
            return redirect('register')
        if User.objects.filter(email=email):
            messages.error(request, "Cet email a déjà un compte")
            return redirect('register')
        if not username.isalnum():
            messages.error(request, "Le nom doit être alphanumérique")
            return redirect('register')
        if password != password1:
            messages.error(request, "Les daux mots de passe ne sont pas les même")
            return redirect('register')
        mon_utilisateur = User.object.create_user(username, email, password)
        mon_utilisateur.first_name = firstname
        mon_utilisateur.last_name = lastname
        mon_utilisateur.is_active = False
        mon_utilisateur.save()
        messages.success(request, 'Votre compte a été créé avec succès')
        # Envoi d'email de bienvenue
        subject = "Bienvenue sur 'le nom du site de rencontre'"
        message = "Bienvenue" + mon_utilisateur.first_name + " " + mon_utilisateur.last_name + "\n Nous sommes heureux de vous compter parmis nos utilistaeur\n\n\n Merci \n\n L'équipe de 'le nom de l'appli'"
        email_sender = settings.EMAIL_HOST_USER
        receivers_list = [mon_utilisateur.email]
        send_mail(subject, message, email_sender, receivers_list, fail_silently=False)
        # Email de confirmation
        current_site = get_current_site(request)
        subject2 = "Confirmation de l'addresse mail sur 'le nom de l'appli'"
        message2 = render_to_string("emailConfirm.html", {
            'name': mon_utilisateur.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(mon_utilisateur.pk)),
            'token': generatorToken.make_token(mon_utilisateur)
        })

        email = EmailMessage(
            subject2,
            message2,
            settings.EMAIL_HOST_USER,
            [mon_utilisateur.email]
        )
        email.fail_silently = False
        email.send()
        return redirect('login')
    

    return render(request, 'accounts/register.html')

def logIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        my_user = User.objects.get(username=username)
        if user is not None:
            login(request, user)
            firstname = user.first_name
            return render(request, 'accounts/index.html', {'firstname': firstname})
        elif my_user.is_active == False:
            messages.error(request, "Vous n'avez pas activé confirmez votre addresse email. Faites le avant de vous connecter. Merci !")
        else:
            messages.error(request, 'Mauvaise authentification')
            return redirect(login)
    return render(request, 'accounts/login.html')
    
def logOut(request):
    logout(request)
    messages.success(request, 'Vous avez été bien déconnecté')
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generatorToken.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Votre compte a bien été activé. Félicitation ! Connectez vous maintenant !")
        return redirect('login')
    else:
        messages.error(request, "L'activation a échoué !!!! ")
        return redirect('home')