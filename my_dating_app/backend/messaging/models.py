from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    # Ce modèle représente une conversation entre plusieurs utilisateurs.
    participants = models.ManyToManyField(User, related_name='conversations')  # Une conversation peut avoir plusieurs participants.
    created_at = models.DateTimeField(auto_now_add=True)  # Enregistre la date et l'heure de création de la conversation.

    def __str__(self):
        # Méthode spéciale pour représenter l'objet sous forme de chaîne de caractères.
        # Ici, on retourne une chaîne qui décrit les participants de la conversation.
        return f"Conversation between: {', '.join(participant.username for participant in self.participants.all())}"

class Message(models.Model):
    # Ce modèle représente un message envoyé par un utilisateur à un autre.
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')  # L'utilisateur qui envoie le message.
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')  # L'utilisateur destinataire du message.
    content = models.TextField()  # Le contenu textuel du message.
    timestamp = models.DateTimeField(auto_now_add=True)  # Enregistre la date et l'heure d'envoi du message.
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')  # La conversation à laquelle le message appartient.

    def __str__(self):
        # Méthode spéciale pour représenter l'objet sous forme de chaîne de caractères.
        # Ici, on retourne une chaîne qui décrit l'expéditeur, le destinataire et l'heure d'envoi du message.
        return f"From: {self.sender.username}, To: {self.recipient.username}, Sent at: {self.timestamp:%Y-%m-%d %H:%M:%S}"
