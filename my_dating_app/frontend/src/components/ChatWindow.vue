<template>
  <!-- Vue template pour afficher la fenêtre de chat -->
  <div class="chat-window">
      <!-- Affichage des messages -->
      <ul class="message-list">
          <!-- Utilisation de v-for pour parcourir les messages -->
          <li v-for="message in messages" :key="message.id" :class="{ 'sent': message.sender === currentUser.id, 'received': message.sender !== currentUser.id }">
              <!-- Affichage du nom de l'expéditeur, contenu du message et heure d'envoi -->
              <div class="message-sender">{{ message.sender }}</div>
              <div class="message-content">{{ message.content }}</div>
              <div class="message-time">{{ formatTime(message.timestamp) }}</div>
          </li>
      </ul>

      <!-- Zone de saisie de texte et bouton d'envoi -->
      <MessageInput @message-sent="sendMessage"></MessageInput>
  </div>
</template>

<script>
import MessageInput from './MessageInput.vue'; // Import du composant de saisie de message
import WebSocketInstance from '../services/WebSocketService.js'; // Import du service WebSocket

export default {
  components: {
      MessageInput
  },
  data() {
      return {
          messages: [], // Tableau pour stocker les messages affichés
          currentUser: { id: 1, name: 'User' }, // Utilisateur actuel, à remplacer par les données de l'utilisateur connecté
          recipientId: 2 // ID du destinataire, à définir dynamiquement
      };
  },
  methods: {
      // Fonction pour formater l'heure d'un message
      formatTime(timestamp) {
          return new Date(timestamp).toLocaleTimeString();
      },
      // Fonction pour envoyer un message
      sendMessage(messageContent) {
          // Envoyer le nouveau message au serveur via WebSocket
          WebSocketInstance.newChatMessage({
              content: messageContent,
              sender: this.currentUser.id,
              recipient: this.recipientId // Assurez-vous de définir recipientId correctement
          });
      },
      // Fonction pour gérer l'arrivée d'un nouveau message
      onNewChatMessage(message) {
          this.messages.push(message);
      },
      // Fonction pour gérer l'envoi d'un message
      onMessageSent(message) {
          this.messages.push(message);
      }
  },
  created() {
      // Initialiser les IDs de l'expéditeur et du destinataire
      const senderId = this.currentUser.id;
      const recipientId = this.recipientId;

      // Connecter au WebSocket
      WebSocketInstance.connectToWebSocket(senderId, recipientId);

      // Écouter les nouveaux messages reçus via WebSocket
      WebSocketInstance.addCallbacks(
          this.onNewChatMessage.bind(this),
          this.onMessageSent.bind(this)
      );
  },
  beforeDestroy() {
      // Supprimer les écouteurs d'événements lorsque le composant est détruit
      WebSocketInstance.removeCallbacks(
          this.onNewChatMessage.bind(this),
          this.onMessageSent.bind(this)
      );

      // Déconnecter du WebSocket
      WebSocketInstance.disconnect();
  }
};
</script>

<style>
/* Styles pour les messages */
.message-list {
  list-style: none;
  padding: 0;
}

.message-list li {
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 10px;
}

/* Style pour les messages envoyés */
.sent {
  background-color: #DCF8C6;
  align-self: flex-end;
}

/* Style pour les messages reçus */
.received {
  background-color: #FFFFFF;
}

/* Style pour le nom de l'expéditeur */
.message-sender {
  font-weight: bold;
}

/* Style pour l'heure du message */
.message-time {
  font-size: 0.8em;
  color: #888;
}
</style>
