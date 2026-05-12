function attachFile() {
    document.getElementById('fileInput').click();
}

async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('room_id', currentChatId);
    
    try {
        const response = await fetch('/chat/upload', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            addMessageToScreen({
                id: Date.now(),
                room_id: currentChatId,
                sender_id: currentUserId,
                content: `📎 Файл: ${file.name}`,
                file_url: data.file_url,
                created_at: new Date().toISOString(),
                is_system: false
            });
        }
    } catch (error) {
        console.error('Upload error:', error);
    }
}

document.getElementById('fileInput')?.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        uploadFile(e.target.files[0]);
    }
    e.target.value = '';
});