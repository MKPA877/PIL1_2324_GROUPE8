class WebSocketService {
    static instance = null; // Instance statique pour le singleton

    callbacks = {}; // Objets de rappel pour gérer les messages reçus

    static getInstance() {
        if (!WebSocketService.instance) {
            WebSocketService.instance = new WebSocketService();
        }
        return WebSocketService.instance;
    }

    constructor() {
        this.socketRef = null; // Référence au WebSocket
    }

    connectToWebSocket(senderId, recipientId) {
        // Création de l'URL de connexion WebSocket
        const chatUrl = `ws://${window.location.host}/ws/chat/${senderId}/${recipientId}/`;
        this.connect(chatUrl);

        // Attendre la réponse du serveur pour confirmer la connexion
        this.waitForSocketConnection(() => {
            console.log('WebSocket connection established.');
        });
    }

    connect(chatUrl) {
        // Connexion au WebSocket
        this.socketRef = new WebSocket(chatUrl);

        // Gestionnaires d'événements WebSocket
        this.socketRef.onopen = () => {
            console.log('WebSocket connection opened.');
        };

        this.socketRef.onmessage = (e) => {
            this.socketNewMessage(e.data);
        };

        this.socketRef.onclose = () => {
            console.log('WebSocket connection closed.');
        };

        this.socketRef.onerror = (e) => {
            console.error('WebSocket error:', e);
        };
    }

    disconnect() {
        // Fermeture de la connexion WebSocket
        if (this.socketRef) {
            this.socketRef.close();
        }
    }

    handleDisconnect() {
        // Gérer la déconnexion du chat
        console.log('Disconnected from chat.');
    }

    socketNewMessage(data) {
        // Gérer les nouveaux messages reçus
        const parsedData = JSON.parse(data);
        const command = parsedData.type;
        if (Object.keys(this.callbacks).length === 0) {
            return;
        }
        if (command === 'user.disconnected') {
            this.handleDisconnect();
        } else if (command === 'chat_message') {
            this.callbacks['chat_message'](parsedData);
        } else if (command === 'new_message') {
            this.callbacks['new_message'](parsedData);
        }
    }

    newChatMessage(message) {
        // Envoyer un nouveau message via WebSocket
        this.sendMessage({
            type: 'chat_message',
            content: message.content,
            sender: message.sender,
            recipient: message.recipient,
        });
    }

    addCallbacks(chatMessageCallback, newMessageCallback) {
        // Ajouter des rappels pour gérer les messages
        this.callbacks['chat_message'] = chatMessageCallback;
        this.callbacks['new_message'] = newMessageCallback;
    }

    removeCallbacks(chatMessageCallback, newMessageCallback) {
        // Supprimer les rappels
        delete this.callbacks['chat_message'];
        delete this.callbacks['new_message'];
    }

    sendMessage(data) {
        // Envoyer un message via WebSocket
        try {
            this.socketRef.send(JSON.stringify({ ...data }));
        } catch (err) {
            console.error('Error sending message', err.message);
        }
    }

    state() {
        // Retourne l'état actuel du WebSocket
        return this.socketRef ? this.socketRef.readyState : WebSocket.CLOSED;
    }

    waitForSocketConnection(callback) {
        // Attendre la connexion WebSocket
        const socket = this.socketRef;
        const recursion = this.waitForSocketConnection;
        setTimeout(() => {
            if (socket.readyState === WebSocket.OPEN) {
                console.log('Connection is made');
                if (callback != null) {
                    callback();
                }
                return;
            } else {
                console.log('Waiting for connection...');
                recursion(callback);
            }
        }, 1);
    }
}

const WebSocketInstance = WebSocketService.getInstance(); // Instance unique du service WebSocket

export default WebSocketInstance; // Export du service WebSocket pour une utilisation dans d'autres modules
