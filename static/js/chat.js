document.addEventListener("DOMContentLoaded", () => {
  const chatbox = document.getElementById("chatbox");
  const chatForm = document.getElementById("chat-form");
  const messageInput = document.getElementById("message-input");
  const sendButton = document.getElementById("send-button");
  const loadingIndicator = document.getElementById("loading-indicator");
  const newChatButton = document.getElementById("new-chat-button");

  // Function to add a message to the chatbox
  function addMessage(message, sender = "user") {
    const messageWrapper = document.createElement("div");
    messageWrapper.classList.add("flex", "animate-slide-in-bottom"); // Add animation class

    const messageElement = document.createElement("div");
    messageElement.classList.add(
      "p-3",
      "rounded-lg",
      "max-w-xs",
      "lg:max-w-md",
      "shadow"
    );

    if (sender === "user") {
      messageWrapper.classList.add("justify-end");
      messageElement.classList.add("bg-primary", "text-white");
    } else {
      // Bot message
      messageWrapper.classList.add("justify-start");
      messageElement.classList.add("bg-secondary", "text-white"); // Different color for bot
    }

    // Support for markdown-like formatting for bot messages
    if (sender === "bot") {
      // Format message with basic markdown-like syntax
      let formattedMessage = message
        // Process code blocks (if any)
        .replace(
          /```([^`]+)```/g,
          '<pre class="bg-gray-800 p-2 rounded text-gray-200 text-sm my-1 overflow-x-auto">$1</pre>'
        )
        // Process bold text
        .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
        // Process italics
        .replace(/\*([^*]+)\*/g, "<em>$1</em>")
        // Process line breaks
        .replace(/\n/g, "<br>");

      messageElement.innerHTML = formattedMessage;
    } else {
      // For user messages, keep using textContent for security
      const messageText = document.createElement("p");
      messageText.textContent = message;
      messageElement.appendChild(messageText);
    }

    messageWrapper.appendChild(messageElement);
    chatbox.appendChild(messageWrapper);

    // Scroll to the bottom
    scrollToBottom();
  }

  // Function to scroll chatbox to the bottom
  function scrollToBottom() {
    chatbox.scrollTop = chatbox.scrollHeight;
  }

  // Function to show/hide loading indicator
  function setLoading(isLoading) {
    if (isLoading) {
      loadingIndicator.classList.remove("hidden");
      sendButton.disabled = true; // Disable button while loading
      messageInput.disabled = true; // Disable input field while loading
    } else {
      loadingIndicator.classList.add("hidden");
      sendButton.disabled = false; // Re-enable button
      messageInput.disabled = false; // Re-enable input field
      messageInput.focus(); // Focus back on input
    }
    scrollToBottom(); // Scroll down to show indicator if needed
  }

  // Function to start a new chat
  function startNewChat() {
    // Effacer tous les messages du chat
    chatbox.innerHTML = "";

    // Ajouter un nouveau message d'accueil
    addMessage(
      "Hello! Ask me anything about the documents I've been trained on.",
      "bot"
    );

    // Focus sur le champ de saisie
    messageInput.value = "";
    messageInput.focus();
  }

  // Handle new chat button click
  if (newChatButton) {
    newChatButton.addEventListener("click", startNewChat);
  }

  // Handle form submission
  chatForm.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent default form submission

    const userMessage = messageInput.value.trim();
    if (!userMessage) return; // Don't send empty messages

    // Display user message immediately
    addMessage(userMessage, "user");

    // Clear the input field
    messageInput.value = "";

    // Show loading indicator
    setLoading(true);

    try {
      // Send message to backend API
      const response = await fetch("/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userMessage }),
      });

      setLoading(false); // Hide loading indicator once response is received

      if (!response.ok) {
        // Handle HTTP errors (e.g., 500 Internal Server Error)
        const errorData = await response
          .json()
          .catch(() => ({ error: "Failed to parse error response." })); // Avoid crashing if error response isn't JSON
        console.error("Error from server:", response.status, errorData);
        addMessage(
          `Sorry, an error occurred: ${errorData.error || "Unknown error"}`,
          "bot"
        );
        return;
      }

      const data = await response.json();
      const botResponse = data.response;

      // Display bot response
      addMessage(botResponse, "bot");
    } catch (error) {
      setLoading(false); // Hide loading indicator on network error
      console.error("Error sending message:", error);
      addMessage(
        "Sorry, I could not connect to the server. Please try again later.",
        "bot"
      );
    }
  });

  // Initial scroll to bottom (in case there are initial messages)
  scrollToBottom();
  messageInput.focus(); // Focus on input on page load
});
