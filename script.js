// API Configuration
const API_BASE_URL = 'http://localhost:5000';

// DOM Elements
const companyNameInput = document.getElementById('companyName');
const websiteUrlInput = document.getElementById('websiteUrl');
const createChatbotBtn = document.getElementById('createChatbot');
const statusMessage = document.getElementById('statusMessage');
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendMessageBtn = document.getElementById('sendMessage');
const chatStatusText = document.getElementById('chatStatusText');

// State
let isChatbotReady = false;
let currentCompanyName = '';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Event listeners
    createChatbotBtn.addEventListener('click', createChatbot);
    sendMessageBtn.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Check if chatbot already exists
    checkChatbotStatus();
});

// Create Chatbot
async function createChatbot() {
    const companyName = companyNameInput.value.trim();
    const websiteUrl = websiteUrlInput.value.trim();

    if (!companyName || !websiteUrl) {
        showError('Please enter both company name and website URL');
        return;
    }

    // Show loading state
    setButtonLoading(createChatbotBtn, true);
    hideStatusMessage();

    try {
        const response = await fetch(`${API_BASE_URL}/create-chatbot`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                company_name: companyName,
                website_url: websiteUrl
            })
        });

        const data = await response.json();

        if (data.success) {
            isChatbotReady = true;
            currentCompanyName = companyName;

            // Show success message
            showStatusMessage(`✅ Connected to API successfully!`, 'success');

            // Update chat status
            chatStatusText.textContent = `Chatbot ready for ${companyName}`;

            // Add system message
            addMessage('bot', `Great! I've analyzed ${companyName}'s website. Ask me anything about the company!`);

            // Clear inputs
            companyNameInput.value = '';
            websiteUrlInput.value = '';

        } else {
            showError(data.error || 'Failed to create chatbot');
        }

    } catch (error) {
        console.error('Error creating chatbot:', error);
        showError('Failed to connect to server. Make sure the Flask backend is running on port 5000.');
    } finally {
        setButtonLoading(createChatbotBtn, false);
    }
}

// Send Message
async function sendMessage() {
    const question = messageInput.value.trim();

    if (!question) {
        return;
    }

    if (!isChatbotReady) {
        showError('Please create a chatbot first by entering a company URL above');
        return;
    }

    // Add user message to chat
    addMessage('user', question);

    // Clear input
    messageInput.value = '';

    // Show typing indicator
    const typingId = addTypingIndicator();

    // Disable send button
    sendMessageBtn.disabled = true;

    try {
        const startTime = Date.now();

        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        // Remove typing indicator
        removeTypingIndicator(typingId);

        if (data.success) {
            const responseTime = Date.now() - startTime;

            // Add bot response
            addMessage('bot', data.response, responseTime);

            // Log response time
            console.log(`Response time: ${data.response_time_ms}ms (Total: ${responseTime}ms)`);

        } else {
            addMessage('bot', `Sorry, I encountered an error: ${data.error}`);
        }

    } catch (error) {
        console.error('Error sending message:', error);
        removeTypingIndicator(typingId);
        addMessage('bot', 'Sorry, I couldn\'t process your question. Please try again.');
    } finally {
        sendMessageBtn.disabled = false;
        messageInput.focus();
    }
}

// Check Chatbot Status
async function checkChatbotStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/chatbot-status`);
        const data = await response.json();

        if (data.ready) {
            isChatbotReady = true;
            currentCompanyName = data.company_name;
            chatStatusText.textContent = `Chatbot ready for ${data.company_name}`;
            showStatusMessage(`✅ Connected to API successfully!`, 'success');
        }
    } catch (error) {
        console.log('No existing chatbot found');
    }
}

// UI Helper Functions
function addMessage(type, text, responseTime = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;

    const icon = type === 'bot' ? '🤖' : '👤';

    let timeText = '';
    if (responseTime) {
        timeText = `<span class="message-time">Response time: ${responseTime}ms</span>`;
    }

    messageDiv.innerHTML = `
        <div class="message-icon">${icon}</div>
        <div class="message-content">
            <p>${escapeHtml(text)}</p>
            ${timeText}
        </div>
    `;

    chatMessages.appendChild(messageDiv);

    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addTypingIndicator() {
    const typingDiv = document.createElement('div');
    const id = 'typing-' + Date.now();
    typingDiv.id = id;
    typingDiv.className = 'message bot-message';

    typingDiv.innerHTML = `
        <div class="message-icon">🤖</div>
        <div class="message-content">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;

    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return id;
}

function removeTypingIndicator(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
    }
}

function showStatusMessage(message, type = 'success') {
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type === 'error' ? 'error-message' : ''}`;
    statusMessage.style.display = 'block';
}

function hideStatusMessage() {
    statusMessage.style.display = 'none';
}

function showError(message) {
    showStatusMessage(`❌ ${message}`, 'error');

    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideStatusMessage();
    }, 5000);
}

function setButtonLoading(button, isLoading) {
    const btnText = button.querySelector('.btn-text');
    const btnLoader = button.querySelector('.btn-loader');

    if (isLoading) {
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-block';
        button.disabled = true;
    } else {
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
        button.disabled = false;
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Test API Connection on Load
async function testAPIConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/`);
        const data = await response.json();
        console.log('API Status:', data);
    } catch (error) {
        console.warn('API not reachable. Make sure Flask server is running.');
    }
}

testAPIConnection();
