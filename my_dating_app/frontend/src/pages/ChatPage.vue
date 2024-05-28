<template>
    <div class="chat-page">
      <!-- Affichage de la fenêtre de chat -->
      <ChatWindow :messages="messages" :currentUser="currentUser" />
  
      <!-- Zone de saisie pour envoyer des messages -->
      <MessageInput @sendMessage="handleSendMessage" />
    </div>
  </template>
  
  <script>
  import ChatWindow from '@/components/ChatWindow.vue';
  import MessageInput from '@/components/MessageInput.vue';
  import WebSocketInstance from '@/services/WebSocketService.js';
  
  export default {
    components: {
      ChatWindow,
      MessageInput
    },
    data() {
      return {
        messages: [], // Tableau pour stocker les messages reçus
        currentUser: { id: 1, name: 'User' }, // Remplacez par les données de l'utilisateur connecté
        chatUrl: 'example_chat_room' // URL de la salle de chat (à adapter selon votre configuration)
      };
    },
    methods: {
      handleSendMessage(messageContent) {
        // Envoyer le nouveau message au serveur via WebSocket
        WebSocketInstance.newChatMessage({
          from: this.currentUser.id,
          message: messageContent,
          recipient_id: 2, // Remplacez par l'ID du destinataire
          conversation_id: 1 // Remplacez par l'ID de la conversation
        });
      },
      onNewChatMessage(message) {
        // Ajouter le nouveau message à la liste des messages
        this.messages.push(message);
      }
    },
    created() {
      // Établir la connexion WebSocket à la création du composant
      WebSocketInstance.connect(this.chatUrl);
  
      // Attendre que la connexion soit établie
      WebSocketInstance.waitForSocketConnection(() => {
        console.log('WebSocket connection established.');
      });
  
      // Ajouter des callbacks pour gérer les nouveaux messages
      WebSocketInstance.addCallbacks(
        this.onNewChatMessage
      );
    },
    beforeDestroy() {
      // Fermer la connexion WebSocket avant de détruire le composant
      WebSocketInstance.disconnect();
    }
  };
  </script>
  
  <style scoped>
  .chat-page {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }
  
  .chat-page .chat-window {
    flex: 1;
    overflow-y: auto;
  }
  
  .chat-page .message-input {
    border-top: 1px solid #ddd;
    padding: 10px;
  }
  </style>
  