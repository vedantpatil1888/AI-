const messagesEl = document.getElementById("messages");
const form = document.getElementById("chatForm");
const input = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");

const WELCOME = "Hello! I'm the college help desk bot. Ask me about admissions, fees, courses, hostel, placements, scholarships, library, transport or contact details. You can also tap a popular question on the left.";

function timeNow() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function addMessage(text, who, extraClass = "") {
  const div = document.createElement("div");
  div.className = `msg ${who} ${extraClass}`.trim();
  div.textContent = text;
  const t = document.createElement("span");
  t.className = "time";
  t.textContent = timeNow();
  div.appendChild(t);
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return div;
}

function showTyping() {
  const div = document.createElement("div");
  div.className = "msg bot typing";
  div.innerHTML = "<span></span><span></span><span></span>";
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return div;
}

async function sendMessage(text) {
  text = text.trim();
  if (!text) return;
  addMessage(text, "user");
  input.value = "";
  sendBtn.disabled = true;
  const typing = showTyping();

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });
    const data = await res.json();
    await new Promise((r) => setTimeout(r, 400)); // short pause so the typing dots are visible
    typing.remove();
    if (!res.ok) {
      addMessage(data.error || "Something went wrong. Please try again.", "bot", "error");
    } else {
      addMessage(data.reply, "bot");
    }
  } catch (err) {
    typing.remove();
    addMessage("Could not reach the server. Check that app.py is running, then try again.", "bot", "error");
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  sendMessage(input.value);
});

document.querySelectorAll(".chip").forEach((chip) => {
  chip.addEventListener("click", () => sendMessage(chip.textContent));
});

clearBtn.addEventListener("click", () => {
  messagesEl.innerHTML = "";
  addMessage(WELCOME, "bot");
  input.focus();
});

addMessage(WELCOME, "bot");
input.focus();
