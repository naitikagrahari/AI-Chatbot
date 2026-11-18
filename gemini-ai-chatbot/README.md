# Gemini AI Chatbot (Python & Flask)

A lightweight, responsive web-based AI chatbot built using **Python**, **Flask**, and the **Google GenAI SDK (`gemini-2.5-flash`)**.

## Features
- **Conversational Memory:** Remembers context from previous messages in the session.
- **Clean Dark UI:** Responsive chat interface built directly into Flask.
- **Secure API Handling:** Uses environment variables (`GEMINI_API_KEY`) so your API key stays safe when pushing to GitHub.

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/gemini-ai-chatbot.git
   cd gemini-ai-chatbot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Gemini API Key:**
   - **Windows (PowerShell):**
     ```powershell
     $env:GEMINI_API_KEY="your_api_key_here"
     ```
   - **Windows (CMD):**
     ```cmd
     set GEMINI_API_KEY="your_api_key_here"
     ```
   - **Mac / Linux:**
     ```bash
     export GEMINI_API_KEY="your_api_key_here"
     ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. Open your browser and visit `http://127.0.0.1:5000`.
