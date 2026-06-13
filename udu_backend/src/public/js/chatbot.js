document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('chatbot-toggle-btn');
    const closeBtn = document.getElementById('chatbot-close-btn');
    const chatWindow = document.getElementById('chatbot-window');
    const sendBtn = document.getElementById('chatbot-send-btn');
    
    const inputField = document.getElementById('chatbot-input-field');
    const messagesBox = document.getElementById('chatbot-messages');

    toggleBtn.addEventListener('click', () => chatWindow.classList.remove('hidden'));
    closeBtn.addEventListener('click', () => chatWindow.classList.add('hidden'));

    const sendMessage = async () => {
        const text = inputField.value.trim();
        if (!text) return;

        appendMessage(text, 'user-message');
        inputField.value = '';

        sendBtn.disabled = true;

        try { 
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: text })
            });
            const data = await response.json();

            appendMessage(data.answer, 'bot-message');
        } catch (error) {
            appendMessage('Xin lỗi, đã xảy ra lỗi khi kết nối với chatbot.', 'bot-message');
        } finally {
            sendBtn.disabled = false;
        };
    };

    sendBtn.addEventListener('click', sendMessage);
    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    function appendMessage(text, className) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${className}`;
        msgDiv.textContent = text;
        messagesBox.appendChild(msgDiv);
        messagesBox.scrollTop = messagesBox.scrollHeight;
    }
});