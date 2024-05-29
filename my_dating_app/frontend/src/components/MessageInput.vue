<template>
  <!-- Vue template pour afficher la zone de saisie de message -->
  <div>
      <!-- Zone de saisie de texte et bouton d'envoi -->
      <input type="text" v-model="newMessage" placeholder="Entrez votre message..."> <!-- Champ de saisie de texte lié à la variable newMessage -->
      <button @click="sendMessage">Envoyer</button> <!-- Bouton d'envoi avec un gestionnaire d'événement @click -->
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
            this.$emit('message-sent', this.newMessage); // Émet un événement 'message-sent' avec le contenu du nouveau message
            // Effacer le champ de saisie après l'envoi du message
            this.newMessage = ''; // Réinitialise le champ de saisie de texte à une chaîne vide
        }
    }
  };
</script>
