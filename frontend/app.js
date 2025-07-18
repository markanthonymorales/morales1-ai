async function send() {
  const msg = document.getElementById("message").value;
  document.getElementById("messages").innerHTML += `<div><b>You:</b> ${msg}</div>`;
  const res = await fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: msg })
  });
  const data = await res.json();
  document.getElementById("messages").innerHTML += `<div><b>Morales1:</b> ${data.response}</div>`;
}
