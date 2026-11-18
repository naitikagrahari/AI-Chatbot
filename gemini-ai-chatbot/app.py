import os
from flask import Flask, request, jsonify, render_template_string
from google import genai
from google.genai import errors

app = Flask(__name__)

# Automatically reads GEMINI_API_KEY from your environment variables
client = genai.Client()

# Maintains conversation context across messages
chat_session = client.chats.create(model="gemini-2.5-flash")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini AI Chatbot</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, -apple-system, sans-serif; }
        body { background-color: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .chat-wrapper { width: 95%; max-width: 500px; height: 85vh; background: #1e293b; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); display: flex; flex-direction: column; overflow: hidden; border: 1px solid #334155; }
        .header { background: #2563eb; padding: 18px; text-align: center; font-size: 1.2rem; font-weight: 600; }
        .chat-box { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; }
        .msg { padding: 12px 16px; border-radius: 14px; max-width: 80%; line-height: 1.5; font-size: 0.95rem; word-wrap: break-word; white-space: pre-wrap; }
        .user { background: #2563eb; color: white; align-self: flex-end; border-bottom-right-radius: 4px; }
        .bot { background: #334155; color: #f1f5f9; align-self: flex-start; border-bottom-left-radius: 4px; }
        .input-container { display: flex; padding: 12px; background: #0f172a; border-top: 1px solid #334155; gap: 8px; }
        input { flex: 1; padding: 12px 16px; border-radius: 25px; border: 1px solid #475569; background: #1e293b; color: white; outline: none; font-size: 1rem; }
        input:focus { border-color: #2563eb; }
        button { background: #2563eb; color: white; border: none; padding: 0 22px; border-radius: 25px; font-weight: 600; cursor: pointer; }
        button:hover { background: #1d4ed8; }
    </style>
</head>
<body>
    <div class="chat-wrapper">
        <div class="header">Gemini AI Chatbot</div>
        <div class="chat-box" id="chat-box">
            <div class="msg bot">Hello! I am your Gemini AI Assistant. How can I help you today?</div>
        </div>
        <div class="input-container">
            <input type="text" id="user-input" placeholder="Type your message..." onkeypress="if(event.key==='Enter') sendMessage()">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById("user-input");
            const chatBox = document.getElementById("chat-box");
            const text = input.value.trim();
            if (!text) return;

            const userDiv = document.createElement("div");
            userDiv.className = "msg user";
            userDiv.textContent = text;
            chatBox.appendChild(userDiv);

            input.value = "";
            chatBox.scrollTop = chatBox.scrollHeight;

            const loadDiv = document.createElement("div");
            loadDiv.className = "msg bot";
            loadDiv.textContent = "Thinking...";
            chatBox.appendChild(loadDiv);
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const res = await fetch("/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: text })
                });
                const data = await res.json();
                loadDiv.textContent = data.reply;
            } catch (err) {
                loadDiv.textContent = "Server error: Please try again.";
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_msg = data.get("message", "").strip()
    if not user_msg:
        return jsonify({"reply": "Please enter a message."}), 400

    try:
        response = chat_session.send_message(user_msg)
        return jsonify({"reply": response.text})
    except errors.APIError as e:
        return jsonify({"reply": f"API Error: {e.message}"}), 500
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
