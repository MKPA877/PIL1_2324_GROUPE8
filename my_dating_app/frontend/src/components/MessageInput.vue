<template>
    <div>
      <!-- Zone de saisie de texte et bouton d'envoi -->
      <input type="text" v-model="newMessage" placeholder="Entrez votre message...">
      <button @click="sendMessage">Envoyer</button>
    </div>
</template>
  
<script>
  export default {
    data() {
      return {
        newMessage: '' // Stocke le nouveau message saisi par l'utilisateur
      };
    },
    methods: {
      sendMessage() {
        // Émettre un événement pour informer le parent de l'envoi d'un nouveau message
        this.$emit('message-sent', this.newMessage);
        // Effacer le champ de saisie après l'envoi du message
        this.newMessage = '';
      }
    }
  };
</script>
  