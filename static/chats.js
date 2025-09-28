let messages = [
    {
      id: "1",
      text: "Hello! I'm FRIDAY, your virtual assistant. How can I help you today?",
      sender: "assistant",
      timestamp: getCurrentTime(),
    },
  ];
  
  // DOM elements
  const messagesContainer = document.getElementById("messagesContainer");
  const messageInput = document.getElementById("messageInput");
  const sendBtn = document.getElementById("sendBtn");
  
  // Initialize lucide icons
  document.addEventListener("DOMContentLoaded", function() {
    lucide.createIcons();
    updateSendButton();
    messageInput.addEventListener("input", updateSendButton);
  });
  
  // Get current time
  function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
    });
  }
  
  // Update send button state
  function updateSendButton() {
    const hasText = messageInput.value.trim().length > 0;
    sendBtn.disabled = !hasText;
  }
  
  // Auto resize textarea
  function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 128) + 'px';
    updateSendButton();
  }
  
  // Scroll to bottom
  function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }
  
  // Create message element
  function createMessageElement(message) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${message.sender}-message`;
    messageDiv.innerHTML = `
      <div class="message-avatar">
        <i data-lucide="${message.sender === 'user' ? 'user' : 'bot'}"></i>
      </div>
      <div class="message-content">
        <div class="message-bubble ${message.sender}-bubble">
          <p>${message.text}</p>
        </div>
        <span class="message-timestamp">${message.timestamp}</span>
      </div>
    `;
    return messageDiv;
  }
  
  // Add message to chat
  function addMessage(message) {
    messages.push(message);
    const messageElement = createMessageElement(message);
    messagesContainer.appendChild(messageElement);
    
    // Re-initialize lucide icons for new elements
    lucide.createIcons();
    
    setTimeout(scrollToBottom, 50);
  }
  
  
  // Send message
  async function sendMessage() {
    const text = messageInput.value.trim();
    if (!text) return;
  
    const userMessage = {
      id: Date.now().toString(),
      text: text,
      sender: "user",
      timestamp: getCurrentTime(),
    };
  
    addMessage(userMessage);
    messageInput.value = "";
    messageInput.style.height = "auto";
    updateSendButton();
  
    try {
      // Send message to Django backend
      const response = await fetch("/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"), // required for Django
        },
        body: JSON.stringify({ message: text }),
      });
  
      const data = await response.json();
  
      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        text: data.response || data.error || "⚠️ No response from assistant.",
        sender: "assistant",
        timestamp: getCurrentTime(),
      };
  
      addMessage(assistantMessage);
    } catch (error) {
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        text: "⚠️ Error connecting to server.",
        sender: "assistant",
        timestamp: getCurrentTime(),
      };
      addMessage(errorMessage);
    }
  }
  

  
    // Simulate assistant response
    setTimeout(() => {
      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        text: "Based on your input, I can suggest several approaches.",
        sender: "assistant",
        timestamp: getCurrentTime(),
      };
      addMessage(assistantMessage);
    }, 1000);
  
  
  // Handle keyboard shortcuts
  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  }
  
  // Clear chat
  function clearChat() {
    // Clear messages array but keep initial message
    messages = [
      {
        id: "1",
        text: "Hello! I'm FRIDAY, your virtual assistant. How can I help you today?",
        sender: "assistant",
        timestamp: getCurrentTime(),
      },
    ];
  
    // Clear messages container and add initial message
    messagesContainer.innerHTML = "";
    const initialMessage = createMessageElement(messages[0]);
    messagesContainer.appendChild(initialMessage);
    
    // Re-initialize lucide icons
    lucide.createIcons();
    
    scrollToBottom();
  }
 
  
  // Get CSRF token (needed for Django POST requests)
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
