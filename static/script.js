const chatWindow = document.getElementById('chat-window');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

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

    // typing indicator, thinking animation
    const typing = document.getElementById('div');
    typing.className = 'typing-indicator';
    typing.innerHTML = '<span></span><span></span><span></span>';
    chatWindow.appendChild(typing);
    chatWindow.scrollTop = chatWindow.scrollHeight;

    const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json '},
        body: JSON.stringify({ message: text })
    });

    const data = await res.json();

    //remove the animation before showing the message
    chatWindow.removeChild(typing);

    addMessage(data.response, 'bot-message');
}

sendBtn.addEventListener('click', sendMessage);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});