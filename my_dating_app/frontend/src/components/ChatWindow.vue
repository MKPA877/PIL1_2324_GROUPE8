<template>
    <div class="chat-window">
      <!-- Affichage des messages -->
      <ul class="message-list">
        <li v-for="message in messages" :key="message.id" :class="{ 'sent': message.sender === currentUser.id, 'received': message.sender !== currentUser.id }">
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
  import MessageInput from './MessageInput.vue'; // Importer le composant MessageInput
  import WebSocketInstance from '../services/WebSocketService.js'; // Importer le service WebSocket
  
  export default {
    components: {
      MessageInput
    },
    data() {
      return {
        messages: [], // Liste des messages à afficher
        currentUser: { id: 1, name: 'User' } // Utilisateur actuel, à remplacer par les données de l'utilisateur connecté
      };
    },
    methods: {
      formatTime(timestamp) {
        // Fonction pour formater l'heure d'envoi du message (à personnaliser selon vos besoins)
        return new Date(timestamp).toLocaleTimeString();
      },
      sendMessage(messageContent) {
        // Envoyer le nouveau message au serveur via WebSocket
        WebSocketInstance.newChatMessage({
          content: messageContent
        });
      }
    },
    created() {
      // Écouter les nouveaux messages reçus via WebSocket
      WebSocketInstance.addCallbacks(
        this.onNewChatMessage.bind(this)
      );
    },
    destroyed() {
      // Supprimer les écouteurs d'événements lorsque le composant est détruit
      WebSocketInstance.removeCallbacks(
        this.onNewChatMessage.bind(this)
      );
    },
    methods: {
      onNewChatMessage(message) {
        // Ajouter le nouveau message à la liste des messages
        this.messages.push(message);
      }
    }
  };
</script>
  
<style>
/* Styles CSS pour la mise en forme des messages */
.message-list {
  list-style: none;
  padding: 0;
}

.message-list li {
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 10px;
}

.sent {
  background-color: #DCF8C6; /* Couleur de fond pour les messages envoyés par l'utilisateur actuel */
  align-self: flex-end;
}

.received {
  background-color: #FFFFFF; /* Couleur de fond pour les messages reçus des autres utilisateurs */
}

.message-sender {
  font-weight: bold;
}

.message-time {
  font-size: 0.8em;
  color: #888;
}
</style>
  