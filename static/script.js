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