function updateCategory(category) {
    document.getElementById('category-text').textContent = category;
}

document.getElementById('image-upload').addEventListener('change', function (e) {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) throw new Error('Upload failed');
            return response.json();
        })
        .then(data => {
            // Update UI with results
            document.getElementById('image-preview').innerHTML = `
            <img src="${data.image_url}" class="preview-image">
        `;
            document.getElementById('image-results').innerHTML = `
            <p>Detected: ${data.prediction} (${data.confidence}%)</p>
        `;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Image upload failed');
        });
});

function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (!message) return;

    input.value = '';
    appendMessage('user', message);

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    })
        .then(response => {
            if (!response.ok) throw new Error('Chat failed');
            return response.json();
        })
        .then(data => {
            appendMessage('bot', data.response);
        })
        .catch(error => {
            console.error('Error:', error);
            appendMessage('bot', "Sorry, I'm having trouble responding right now.");
        });
}

function appendMessage(sender, text) {
    const chatHistory = document.getElementById('chat-history');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.textContent = text;
    chatHistory.appendChild(messageDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}