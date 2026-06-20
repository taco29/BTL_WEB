document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('chatbot-toggle-btn');
    const closeBtn = document.getElementById('chatbot-close-btn');
    const chatWindow = document.getElementById('chatbot-window');
    const sendBtn = document.getElementById('chatbot-send-btn');
    
    const inputField = document.getElementById('chatbot-input-field');
    const messagesBox = document.getElementById('chatbot-messages');
    const scrollBottomBtn = document.getElementById('chatbot-scroll-bottom-btn');

    const tooltip = toggleBtn.querySelector('.chatbot-tooltip');

    let typingElement = null;

    toggleBtn.addEventListener('click', () => {
        chatWindow.classList.remove('hidden');
        if (tooltip) tooltip.style.display = 'none';
    });
    closeBtn.addEventListener('click', () => {
        chatWindow.classList.add('hidden');
        if (tooltip) tooltip.style.display = '';
    });

    function scrollToBottom() {
        messagesBox.scrollTo({
            top: messagesBox.scrollHeight,
            behavior: 'smooth'
        });
    }

    scrollBottomBtn.addEventListener('click', scrollToBottom);

    messagesBox.addEventListener('scroll', () => {
        const isNearBottom = messagesBox.scrollHeight - messagesBox.scrollTop - messagesBox.clientHeight < 50;
        if (isNearBottom) {
            scrollBottomBtn.classList.add('hidden'); 
        } else {
            scrollBottomBtn.classList.remove('hidden'); 
        }
    });

    function showTyping() {
        typingElement = document.createElement('div');
        typingElement.className = 'message bot-message typing-indicator';
        typingElement.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
        messagesBox.appendChild(typingElement);
        messagesBox.scrollTop = messagesBox.scrollHeight;
    }

    function removeTyping() {
        if (typingElement) {
            messagesBox.removeChild(typingElement);
            typingElement = null;
        }
    }
    
    const sendMessage = async () => {
        const text = inputField.value.trim();
        if (!text) return;

        appendMessage(text, 'user-message');
        inputField.value = '';

        sendBtn.disabled = true;

        showTyping();
        
        try { 
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: text })
            });
            const data = await response.json();

            removeTyping();

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

    function formatBotText(text) {
        return text
            .split('\n')
            .map(line => {
                const escaped = line
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;');
                if (/^\d+\./.test(line.trim())) {
                    return `<span class="chat-section-title">${escaped}</span>`;
                }
                if (/^(\s+[\-a-zA-Z]|\s{2,})/.test(line)) {
                    return `<span class="chat-indent">${escaped}</span>`;
                }
                return `<span>${escaped}</span>`;
            })
            .join('<br>');
    }

    function appendMessage(text, className) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${className}`;
        if (className === 'bot-message') {
            msgDiv.innerHTML = formatBotText(text);
        } else {
            msgDiv.textContent = text;
        }
        messagesBox.appendChild(msgDiv);
        scrollToBottom();
    } 
});