const currentUserId = {{ user.id }};
let currentChatId = null;
let socket = null;

async function loadChats() {
    const response = await fetch('/chat/chats');
    const chats = await response.json();
    const container = document.getElementById('chatsList');
    container.innerHTML = '';
    
    for (const chat of chats) {
        const chatDiv = document.createElement('div');
        chatDiv.className = 'chat-item' + (currentChatId === chat.id ? ' active' : '');
        chatDiv.setAttribute('data-chat-id', chat.id);
        chatDiv.onclick = () => selectChat(chat.id);
        chatDiv.innerHTML = `
            <div class="chat-name">${chat.name} ${chat.is_private ? '🔒' : '👥'}</div>
            <div class="chat-preview">${chat.last_message || 'Новое сообщение'}</div>
        `;
        container.appendChild(chatDiv);
    }
}

function addMessageToScreen(message) {
    const container = document.getElementById('messages');
    const welcome = container.querySelector('.welcome');
    if (welcome) welcome.remove();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${message.is_system ? 'system-message' : (message.sender_id === currentUserId ? 'my-message' : 'other-message')}`;
    messageDiv.innerHTML = `
        <div class="message-bubble">
            ${!message.is_system && message.sender_id !== currentUserId ? `<div class="message-name">Пользователь ${message.sender_id}</div>` : ''}
            ${message.content}
            <div class="message-time">${new Date(message.created_at).toLocaleTimeString()}</div>
        </div>
    `;
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

async function loadMessages(chatId) {
    const response = await fetch(`/chat/${chatId}/messages`);
    const messages = await response.json();
    
    const container = document.getElementById('messages');
    container.innerHTML = '';
    
    if (messages.length === 0) {
        container.innerHTML = '<div class="welcome">Напишите первое сообщение!</div>';
    } else {
        for (const msg of messages) {
            addMessageToScreen(msg);
        }
    }
}

async function startPrivateChat() {
    const userId = document.getElementById('searchId').value;
    if (!userId) {
        alert('Введите ID пользователя');
        return;
    }
    
    if (parseInt(userId) === currentUserId) {
        alert('Нельзя начать чат с самим собой');
        return;
    }
    
    const response = await fetch(`/chat/private/create/${userId}`, {
        method: 'POST'
    });
    
    if (response.ok) {
        const room = await response.json();
        document.getElementById('searchId').value = '';
        await loadChats();
        selectChat(room.id);
    } else {
        alert('Пользователь не найден');
    }
}

function showGroupModal() {
    document.getElementById('overlay').style.display = 'block';
    document.getElementById('groupModal').style.display = 'block';
}

function closeGroupModal() {
    document.getElementById('overlay').style.display = 'none';
    document.getElementById('groupModal').style.display = 'none';
    document.getElementById('groupName').value = '';
    document.getElementById('groupDesc').value = '';
}

async function createGroup() {
    const name = document.getElementById('groupName').value;
    const description = document.getElementById('groupDesc').value;
    
    if (!name) {
        alert('Введите название группы');
        return;
    }
    
    const response = await fetch('/chat/groups/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, description })
    });
    
    if (response.ok) {
        const room = await response.json();
        closeGroupModal();
        await loadChats();
        selectChat(room.id);
    } else {
        alert('Ошибка создания группы');
    }
}

async function selectChat(chatId) {
    if (!chatId) return;
    
    currentChatId = chatId;
    
    const infoResponse = await fetch(`/chat/${chatId}/info`);
    const chatInfo = await infoResponse.json();
    
    document.getElementById('chatHeader').innerHTML = `
        <span>💬 ${chatInfo.name || 'Чат'}</span>
        <div class="room-actions">
            <button class="add-member" onclick="addMember()">➕ Добавить участника</button>
            <button class="leave-chat" onclick="leaveChat()">🚪 Покинуть чат</button>
        </div>
    `;
    document.getElementById('messageInput').disabled = false;
    document.getElementById('sendButton').disabled = false;
    
    await loadMessages(chatId);
    connectWebSocket();
    
    document.querySelectorAll('.chat-item').forEach(item => {
        item.classList.remove('active');
        if (parseInt(item.getAttribute('data-chat-id')) === chatId) {
            item.classList.add('active');
        }
    });
}

async function addMember() {
    const userId = prompt('Введите ID пользователя для добавления в группу:');
    if (userId && currentChatId) {
        const response = await fetch(`/chat/${currentChatId}/add_member/${userId}`, {
            method: 'POST'
        });
        const result = await response.json();
        alert(result.message);
        if (response.ok) {
            await loadMessages(currentChatId);
        }
    }
}

async function leaveChat() {
    if (confirm('Вы уверены, что хотите покинуть этот чат?')) {
        const response = await fetch(`/chat/${currentChatId}/leave`, {
            method: 'POST'
        });
        if (response.ok) {
            currentChatId = null;
            await loadChats();
            document.getElementById('chatHeader').innerHTML = '<span>💬 Выберите чат</span><div class="room-actions"></div>';
            document.getElementById('messages').innerHTML = '<div class="welcome">Выберите чат для общения</div>';
            document.getElementById('messageInput').disabled = true;
            document.getElementById('sendButton').disabled = true;
            if (socket) socket.close();
        }
    }
}

function connectWebSocket() {
    if (socket) socket.close();
    socket = new WebSocket(`ws://${window.location.host}/chat/ws/${currentUserId}`);
    socket.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        if (msg.room_id === currentChatId) {
            addMessageToScreen(msg);
            loadChats();
        }
    };
}

async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (message && currentChatId) {
        const tempMessage = {
            id: Date.now(),
            room_id: currentChatId,
            sender_id: currentUserId,
            content: message,
            created_at: new Date().toISOString(),
            is_system: false
        };
        
        addMessageToScreen(tempMessage);
        input.value = '';
        
        const response = await fetch(`/chat/${currentChatId}/messages`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content: message })
        });
        
        if (response.ok) {
            loadChats();
        }
    }
}

document.getElementById('sendButton').onclick = sendMessage;
document.getElementById('messageInput').onkeypress = (e) => {
    if (e.key === 'Enter') sendMessage();
};

loadChats();