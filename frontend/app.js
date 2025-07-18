document.addEventListener("DOMContentLoaded", () => {
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");
  const chatBox = document.getElementById("chat-box");
  const uploadForm = document.getElementById("upload-form");
  const uploadInput = document.getElementById("upload-input");

  // Handle chat submission
  chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;

    appendMessage("You", message);
    chatInput.value = "";

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message })
      });

      const data = await response.json();
      appendMessage("Morales1", data.answer || "No response.");
    } catch (err) {
      console.error("Chat error:", err);
      appendMessage("System", "⚠️ Error connecting to server.");
    }
  });

  // Handle file upload
  uploadForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const file = uploadInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("/upload", {
        method: "POST",
        body: formData
      });

      const result = await response.json();
      if (response.ok) {
        appendMessage("System", `✅ File "${file.name}" uploaded successfully.`);
      } else {
        appendMessage("System", `❌ Upload failed: ${result.error || "Unknown error."}`);
      }
    } catch (err) {
      console.error("Upload error:", err);
      appendMessage("System", "⚠️ Error uploading file.");
    }
  });

  function appendMessage(sender, text) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message");
    msgDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
  }
});
