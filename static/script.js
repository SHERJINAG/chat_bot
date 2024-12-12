function sendMessage() {
    const userMessage = document.getElementById('user-input').value;
    const chatBody = document.getElementById('chat-body');

    if (userMessage.trim() === '') {
        return;
    }

    const userMessageElement = document.createElement('p');
    userMessageElement.className = 'chat-message';
    userMessageElement.textContent = userMessage;

    chatBody.appendChild(userMessageElement);

    document.getElementById('user-input').value = '';

    fetch('/ask', {
        method: 'POST',
        body: new URLSearchParams({ user_input: userMessage }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
    .then(response => response.json())
    .then(data => {
        const chatbotMessageElement = document.createElement('p');
        chatbotMessageElement.className = 'chat-message chatbot-message';
        chatbotMessageElement.textContent = data.response;

        chatBody.appendChild(chatbotMessageElement);

        chatBody.scrollTop = chatBody.scrollHeight;
    });
}
