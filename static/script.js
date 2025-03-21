const chatBox = document.getElementById("chat-box");
const chatInput = document.getElementById("chat-input");

// Handle Enter Key Submission
chatInput.addEventListener("keydown", async (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        const userMessage = chatInput.value.trim();
        if (userMessage) {
            addMessage(userMessage, "user");
            chatInput.value = "";

            // Send message to the server
            try {
                const response = await fetch("/process", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ text: userMessage }),
                });

                const result = await response.json();
                if (response.ok) {
                    addMessage(result.response, "bot");
                } else {
                    addMessage(`Error: ${result.error}`, "bot");
                }
            } catch (error) {
                addMessage(`Error: ${error.message}`, "bot");
            }
        } else {
            addMessage("Please enter a message before sending.", "bot");
        }
    }
});

// Add Message to Chat Box
function addMessage(message, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("chat-message", sender);
    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
}