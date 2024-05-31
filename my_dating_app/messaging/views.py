from django.shortcuts import render, get_object_or_404
from .models import Conversation, Message
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponse
from channels.layers import get_channel_layer
from .forms import MessageForm

@login_required   # Garantit que seul un utilisateur authentifié y a accès
def conversation_list(request):  # Vue pour lister les conversations
    conversations = Conversation.objects.filter(participants=request.user)  # Récupère les instances de l'objet conversation et les filtres avec la méthode 'filter' 
    return render(request, 'templates/conversation_list.html', {'conversations': conversations})   # Rend une page html

@login_required   # Garantit que seul un utilisateur authentifié y a accès
def chat_room(request, conversation_id):  # Vue pour la page de chat
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)  # Cette ligne essai de récupérer une instance de l'objet Conversation et si rien n'est trouvé elle renvoie un '404 no found'
    messages = Message.objects.filter(conversation=conversation).order_by('timestamp')  # Cette ligne récupère les messages liés à cette conversation et les tri par ordre croissant
    form = MessageForm()
    return render(request, 'templates/chat_room.html', {
        'conversation': conversation,
        'messages': messages,
        'form': form
    })  # Cette ligne rend une page html

@login_required  # Garantit que seul un utilisateur authentifié y a accès
@require_POST  # Seules les formulaires de type poste déclencheront cette vue
def send_message(request, conversation_id):   # Vue pour envoyer un message
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user) # Cette ligne essai de récupérer une instance de la conversation et renvoi un '404 no found' si rien n'est trouvé
    content = request.POST.get('message')  # Cette ligne extrait le contenu du message envoyé
    if content:
        message = Message(sender=request.user, conversation=conversation, content=content)  # Crée un  nouvelle objet message
        message.save()  # Enregistre l'objet message dans la base de donnée
        # Retourner une réponse HTTP avec un code 200 OK pour indiquer que le message a été envoyé
        return HttpResponse()  # On peut également renvoyer un message ou un JSON pour indiquer le succès si nécessaire
    else:
        # Retourner une réponse HTTP avec un code 400 Bad Request si aucun contenu de message n'est fourni
        return HttpResponseBadRequest("Le contenu du message est vide")

@login_required
def start_new_conversation(request, user_id):   # Vue pour démarrer une nouvelle conversation
    other_user = get_object_or_404(User, id=user_id) # Cette ligne récupère l'objet User correspondant à l'identifiant user_id fourni dans l'UR
    conversation, created = Conversation.objects.get_or_create(participants=[request.user, other_user])  # Cette ligne récupère ou crée une instance de l'objet conversation
    return HttpResponseRedirect(reverse('chat_room', args=[conversation.id]))  # Après avoir créé ou récupéré la conversation, cette ligne redirige l'utilisateur vers la vue de la salle de discussion (chat_room) pour la nouvelle conversation

"""@login_required
def delete_conversation(request, conversation_id):   # Vue pour supprimer une conversation
    conversation = get_object_or_404(Conversation, id=conversation_id)  # Cette ligne cherche la conversation ayant l'id spécifié et retourne un '404 no found' si rien n'est trouvé 
    if request.method == 'POST': # Vérifie si la méthode est de type post 
        if request.user in conversation.participants.all(): # Vérifie si l'utilisateur est dans la discussion actuelle
            conversation.delete() # On supprime la conversation
            messages.success(request, 'Conversation deleted successfully.')  # On envoie un mesage pour signaler la succès de la déletion
            return HttpResponseRedirect(reverse('conversation_list'))  # On retourne à la page de la liste des conversations
        else:
            messages.error(request, 'You are not a participant of this conversation.')  # Si le participant ne fait pas parti de la conversation on le lui notifie
            return HttpResponseRedirect(reverse('conversation_list'))# puis on le renvoie à la page de la liste des conversations
    else:
        messages.error(request, 'Invalid request method.')  # Si la méthode utilisée pour la requête n'est pas un POST on envoie un message pour le notifier
        return HttpResponseRedirect(reverse('conversation_list'))# Puis on redirige vers la liste des conversations

@login_required
def block_user(request, user_id):  # C'est pour bloquer un utilisateur
    user_to_block = get_object_or_404(User, id=user_id)  # Cette ligne recherche l'utilisateur ayant l'id spécifié et retourne un '404 no found' si rien n'est trouvé
    
    # Ajoute l'utilisateur à la liste des utilisateurs bloqués de l'utilisateur connecté
    request.user.blocked_users.add(user_to_block)
    
    # Supprime toutes les conversations avec l'utilisateur bloqué
    Conversation.objects.filter(participants=user_to_block, participants=request.user).delete()
    
    # Ajoute un message de succès
    messages.success(request, f'You have blocked {user_to_block.username}.')
    
    # Redirige l'utilisateur vers une page appropriée (peut-être la liste des utilisateurs)
    return HttpResponseRedirect(reverse('conversation_list.html'))
"""