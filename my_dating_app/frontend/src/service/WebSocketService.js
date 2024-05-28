class WebSocketService {
    static instance = null;
    callbacks = {};

    static getInstance() {
        if (!WebSocketService.instance) {
            WebSocketService.instance = new WebSocketService();
        }
        return WebSocketService.instance;
    }

    constructor() {
        this.socketRef = null;
    }

    connectToWebSocket(chatUrl) {
        this.connect(chatUrl);
        
        // Attente de la réponse du serveur pour confirmer la connexion
        this.waitForSocketConnection(() => {
            console.log('WebSocket connection established.');
            // Afficher un message de connexion réussie ou mettre à jour l'interface utilisateur
        });
    }
    
    

    disconnect() {
        this.socketRef.close();
    }

    handleDisconnect() {
        // Effectuer les actions nécessaires lors de la déconnexion
        console.log('Disconnected from chat.');
        // Rediriger l'utilisateur vers une autre page, si nécessaire
        // window.location.href = '/friends-list/';
    }

    socketNewMessage(data) {
        const parsedData = JSON.parse(data);
        const command = parsedData.type;
        if (Object.keys(this.callbacks).length === 0) {
            return;
        }
        if (command === 'user.disconnected') {
            this.handleDisconnect();
        } else if (command === 'chat_message') {
            this.callbacks[command](parsedData.message);
        }
    }

    fetchMessages(username) {
        this.sendMessage({
            command: 'fetch_messages',
            username: username
        });
    }

    newChatMessage(message) {
        this.sendMessage({
            command: 'new_message',
            from: message.from,
            message: message.content
        });
    }

    addCallbacks(chatMessagesCallback, newMessageCallback) {
        this.callbacks['chat_message'] = chatMessagesCallback;
        this.callbacks['new_message'] = newMessageCallback;
    }

    sendMessage(data) {
        try {
            this.socketRef.send(JSON.stringify({ ...data }));
        } catch (err) {
            console.error('Error sending message', err.message);
        }
    }

    state() {
        return this.socketRef.readyState;
    }

    waitForSocketConnection(callback) {
        const socket = this.socketRef;
        const recursion = this.waitForSocketConnection;
        setTimeout(
            function () {
                if (socket.readyState === 1) {
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

const WebSocketInstance = WebSocketService.getInstance();

export default WebSocketInstance;
