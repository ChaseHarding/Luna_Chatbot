const chatWindow = document.getElementById('chat_window');
const userInput = document.getElementById('user_input');
const sendBtn = document.getElementById('send_btn');

function addMessage (text, sender) {
    const message = document.createElement('div');
    message.textContent = text;
    message.className = sender;
    chatWindow.appendChild(message);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    addMessage(text, 'user-message');
    userInput.value = '';

    const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content_Type': 'application/json '},
        body: JSON.stringify({ message: text })
    });

    const data = await res.json();
    addMessage(data.response, 'bot-message');
}

sendBtn.addEventListener('click', sendMessage);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});