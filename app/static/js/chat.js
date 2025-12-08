/**
 * Chat.js - Centralized Socket.IO Management
 * Handles chat events, lifecycle, Online/Ausente status, and prevents duplicate listeners
 */

class ChatManager {
    constructor() {
        this.socket = null;
        this.isConnected = false;
        this.eventHandlers = new Map();
        this.currentUserId = null;
        this.openChatWindows = {};
        this.unreadMessages = {};
        this.userStatus = 'online'; // online | ausente
    }

    /**
     * Initialize Socket.IO connection
     * @param {number} userId - Current user ID
     */
    init(userId) {
        if (this.socket) {
            console.warn('[Chat] Already initialized');
            return;
        }

        this.currentUserId = userId;
        this.socket = io();
        this.setupEventListeners();
        this.isConnected = true;

        console.log('[Chat] Initialized for user:', userId);
    }

    /**
     * Setup all socket event listeners (centralized)
     */
    setupEventListeners() {
        // Connection events
        this.socket.on('connect', () => {
            console.log('[Chat] Connected to server');
            this.isConnected = true;
            // Immediately set status as online (session is active)
            this.updateStatus('online');
        });

        this.socket.on('disconnect', () => {
            console.log('[Chat] Disconnected from server');
            this.isConnected = false;
        });

        // Online users list
        this.socket.on('online_users', (data) => {
            this.handleOnlineUsers(data);
        });

        // Unread message counts
        this.socket.on('unread_counts', (data) => {
            this.unreadMessages = data;
            this.updateUserListBadges();
            this.checkAllUnread();
        });

        // New messages
        this.socket.on('new_message', (data) => {
            this.handleNewMessage(data);
        });

        // Chat history
        this.socket.on('chat_history', (data) => {
            this.handleChatHistory(data);
        });
    }

    /**
     * Update user status (online/ausente)
     * @param {string} status - 'online' or 'ausente'
     */
    updateStatus(status) {
        if (!this.isConnected) return;

        this.userStatus = status;
        this.socket.emit('update_status', { status });
        console.log(`[Chat] Status updated to: ${status}`);
    }

    /**
     * Handle online users list update
     */
    handleOnlineUsers(data) {
        const onlineUsersList = document.getElementById('online-users-list');
        if (!onlineUsersList) return;

        onlineUsersList.innerHTML = '';

        data.users.forEach(user => {
            if (user.id !== this.currentUserId) {
                const userDiv = this.createUserListItem(user);
                onlineUsersList.appendChild(userDiv);
            }
        });

        if (onlineUsersList.children.length === 0) {
            onlineUsersList.innerHTML = '<p class="text-muted text-center">No hay usuarios conectados</p>';
        }
    }

    /**
     * Create user list item element
     */
    createUserListItem(user) {
        const userDiv = document.createElement('div');
        userDiv.className = 'p-2 border-bottom';
        userDiv.style.cursor = 'pointer';
        userDiv.id = `user-list-item-${user.id}`;

        const unreadCount = this.unreadMessages[user.id] || 0;
        const badgeHtml = unreadCount > 0
            ? `<span class="badge bg-danger rounded-pill ms-auto">${unreadCount}</span>`
            : '';

        const statusText = user.status === 'online' ? 'En línea' : user.status === 'ausente' ? 'Ausente' : 'Fuera de línea';
        const statusColor = user.status === 'online' ? 'text-success' : user.status === 'ausente' ? 'text-warning' : 'text-secondary';
        const statusIcon = user.status === 'online' ? '🟢' : user.status === 'ausente' ? '🟡' : '⚫';

        userDiv.innerHTML = `
      <div class="d-flex align-items-center" style="width: 100%;">
        <img src="/static/${user.profile_picture}" class="rounded-circle me-2" width="40" height="40" style="object-fit: cover;">
        <div>
          <strong>${user.username}</strong>
          <small class="text-muted d-block">${user.role}</small>
          <small class="${statusColor} d-block">${statusIcon} ${statusText}</small>
        </div>
        ${badgeHtml}
      </div>
    `;

        userDiv.onclick = () => this.openChatWindow(user.id, user.username, user.role, user.profile_picture);
        return userDiv;
    }

    /**
     * Handle new message
     */
    handleNewMessage(data) {
        const otherUserId = data.sender_id === this.currentUserId ? data.receiver_id : data.sender_id;
        const messagesDiv = document.getElementById(`messages-${otherUserId}`);

        if (messagesDiv) {
            // Window is open, add message
            this.addMessageToWindow(otherUserId, data);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;

            if (data.receiver_id === this.currentUserId) {
                this.socket.emit('mark_as_read', { sender_id: data.sender_id });
            }
        } else if (data.receiver_id === this.currentUserId) {
            // Window is closed, show notification
            this.showNotification(data);

            // Increment unread count
            this.unreadMessages[data.sender_id] = (this.unreadMessages[data.sender_id] || 0) + 1;
            this.updateUserListBadge(data.sender_id);
        }
    }

    /**
     * Handle chat history
     */
    handleChatHistory(data) {
        const messagesDiv = document.getElementById(`messages-${data.other_user_id}`);
        if (!messagesDiv) return;

        messagesDiv.innerHTML = '';
        data.messages.forEach(msg => {
            this.addMessageToWindow(data.other_user_id, msg);
        });

        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    /**
     * Add message to chat window
     */
    addMessageToWindow(userId, msg) {
        const messagesDiv = document.getElementById(`messages-${userId}`);
        if (!messagesDiv) return;

        const msgDiv = document.createElement('div');
        msgDiv.className = 'mb-2';

        const isOwnMessage = msg.sender_id === this.currentUserId;
        msgDiv.style.textAlign = isOwnMessage ? 'right' : 'left';

        const bgClass = isOwnMessage ? 'bg-primary text-white' : 'bg-light';
        const timeClass = isOwnMessage ? 'text-white-50' : 'text-muted';

        const timestamp = new Date(msg.timestamp).toLocaleTimeString('es-ES', {
            hour: '2-digit',
            minute: '2-digit'
        });

        msgDiv.innerHTML = `
      <div class="${bgClass} d-inline-block px-3 py-2 rounded-3" style="max-width: 70%;">
        <div>${msg.content}</div>
        <small class="${timeClass}">${timestamp}</small>
      </div>
    `;

        messagesDiv.appendChild(msgDiv);
    }

    /**
     * Open chat window
     */
    openChatWindow(userId, username, userRole, userProfilePic) {
        // Clear unread messages
        this.unreadMessages[userId] = 0;
        this.updateUserListBadge(userId);
        this.checkAllUnread();

        if (this.openChatWindows[userId]) {
            this.openChatWindows[userId].style.zIndex = 1000;
            return;
        }

        const chatWindow = this.createChatWindow(userId, username, userProfilePic);
        this.openChatWindows[userId] = chatWindow;

        this.socket.emit('get_chat_history', { user_id: userId });
        this.socket.emit('mark_as_read', { sender_id: userId });
    }

    /**
     * Create chat window element
     */
    createChatWindow(userId, username, userProfilePic) {
        const chatWindowsContainer = document.getElementById('chat-windows-container');
        if (!chatWindowsContainer) {
            console.error('[Chat] chat-windows-container not found');
            return null;
        }

        const chatWindow = document.createElement('div');
        chatWindow.className = 'chat-window card';
        chatWindow.id = `chat-window-${userId}`;
        chatWindow.style.position = 'fixed';
        chatWindow.style.width = '350px';
        chatWindow.style.height = '450px';
        chatWindow.style.zIndex = '999';
        chatWindow.style.bottom = '20px';
        chatWindow.style.right = `${340 + (Object.keys(this.openChatWindows).length * 30)}px`;

        chatWindow.innerHTML = `
      <div class="card-header bg-info text-white d-flex justify-content-between align-items-center">
        <div class="d-flex align-items-center">
          <img src="/static/${userProfilePic}" class="rounded-circle me-2" width="30" height="30" style="object-fit: cover;">
          <strong>${username}</strong>
        </div>
        <button class="btn btn-sm btn-link text-white" onclick="chatManager.closeChatWindow(${userId})">✕</button>
      </div>
      <div class="chat-messages" id="messages-${userId}" style="height: 320px; overflow-y: auto; padding: 10px;"></div>
      <div class="p-2 border-top">
        <div class="input-group input-group-sm">
          <input type="text" id="chat-input-${userId}" class="form-control" placeholder="Escribe un mensaje...">
          <button class="btn btn-primary" onclick="chatManager.sendMessage(${userId})">Enviar</button>
        </div>
      </div>
    `;

        chatWindowsContainer.appendChild(chatWindow);

        // Add enter key listener
        const input = document.getElementById(`chat-input-${userId}`);
        if (input) {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.sendMessage(userId);
                }
            });
        }

        return chatWindow;
    }

    /**
     * Close chat window
     */
    closeChatWindow(userId) {
        const window = this.openChatWindows[userId];
        if (window) {
            window.remove();
            delete this.openChatWindows[userId];
        }
    }

    /**
     * Send message to user
     */
    sendMessage(userId) {
        const input = document.getElementById(`chat-input-${userId}`);
        if (!input) return;

        const msg = input.value.trim();
        if (msg) {
            this.socket.emit('private_message', {
                receiver_id: userId,
                content: msg
            });
            input.value = '';
        }
    }

    /**
     * Update user list badge
     */
    updateUserListBadge(userId) {
        const userListItem = document.getElementById(`user-list-item-${userId}`);
        if (!userListItem) return;

        const existingBadge = userListItem.querySelector('.badge');
        const unreadCount = this.unreadMessages[userId] || 0;

        if (unreadCount > 0) {
            if (existingBadge) {
                existingBadge.textContent = unreadCount;
            } else {
                const badge = document.createElement('span');
                badge.className = 'badge bg-danger rounded-pill ms-auto';
                badge.textContent = unreadCount;
                userListItem.querySelector('.d-flex').appendChild(badge);
            }
        } else {
            if (existingBadge) {
                existingBadge.remove();
            }
        }
    }

    /**
     * Update all user list badges
     */
    updateUserListBadges() {
        for (const userId in this.unreadMessages) {
            this.updateUserListBadge(userId);
        }
    }

    /**
     * Check if there are any unread messages
     */
    checkAllUnread() {
        const totalUnread = Object.values(this.unreadMessages).reduce((a, b) => a + b, 0);
        const chatHeader = document.querySelector('#chat-widget .card-header');

        if (totalUnread > 0 && chatHeader) {
            this.startBlinking(chatHeader);
        } else if (chatHeader) {
            this.stopBlinking(chatHeader);
        }
    }

    /**
     * Start blinking notification
     */
    startBlinking(element) {
        if (element.blinkInterval) return;

        element.blinkInterval = setInterval(() => {
            element.classList.toggle('bg-primary');
            element.classList.toggle('bg-warning');
        }, 500);
    }

    /**
     * Stop blinking notification
     */
    stopBlinking(element) {
        if (element.blinkInterval) {
            clearInterval(element.blinkInterval);
            element.blinkInterval = null;
            element.classList.add('bg-primary');
            element.classList.remove('bg-warning');
        }
    }

    /**
     * Show notification for new message
     */
    showNotification(data) {
        const chatHeader = document.querySelector('#chat-widget .card-header');
        if (chatHeader) {
            const headerSpan = chatHeader.querySelector('span:first-child');
            if (headerSpan) {
                headerSpan.innerText = `💬 Mensaje de ${data.sender_name}`;
            }
            this.startBlinking(chatHeader);
        }
    }

    /**
     * Toggle chat list visibility
     */
    toggleChatList() {
        const chatListBody = document.getElementById('chat-list-body');
        const toggleIcon = document.getElementById('chat-toggle-icon');
        const chatHeader = document.querySelector('#chat-widget .card-header');

        if (!chatListBody || !toggleIcon) return;

        const isOpen = chatListBody.style.display === 'block';

        chatListBody.style.display = isOpen ? 'none' : 'block';
        toggleIcon.innerText = isOpen ? '+' : '-';

        if (!isOpen) {
            // Opening the list
            this.stopBlinking(chatHeader);
            this.socket.emit('get_online_users');
        }
    }

    /**
     * Disconnect and cleanup
     */
    disconnect() {
        if (this.socket) {
            this.socket.disconnect();
            this.socket = null;
            this.isConnected = false;
            console.log('[Chat] Disconnected');
        }
    }

    /**
     * Reconnect (useful for page transitions)
     */
    reconnect() {
        if (!this.socket && this.currentUserId) {
            this.init(this.currentUserId);
        }
    }
}

// Global instance
const chatManager = new ChatManager();

// Expose global function for toggle
function toggleChatList() {
    chatManager.toggleChatList();
}

// Update user status function (called from main.js)
function updateUserStatus(status) {
    chatManager.updateStatus(status);
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    // Don't disconnect on page reload - we want to maintain Online status
    // Only disconnect if explicitly logging out
});
