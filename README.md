# AI Chatbot with Firebase Integration

## Overview
A Python-based AI chatbot using Google's Gemini API and Firebase Firestore for conversation logging.

## Prerequisites
- Python 3.8+
- Google Cloud account with Gemini API enabled
- Firebase project with Firestore
- Internet connection

## Installation
```bash
git clone https://github.com/yourusername/chatbot-project.git
cd chatbot-project
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
Configuration
Create .env file:

bash
echo "GOOGLE_API_KEY=your_api_key_here" > .env
Download Firebase service account key as serviceAccountKey.json and place in project root.

Running the App
bash
python chatbot.py
Access at: http://localhost:5000

Firebase Structure
/conversations
  /{conversation_id}
    - created_at: timestamp
    - updated_at: timestamp
    /messages
      /{message_id}
        - role: "user"|"bot"
        - text: string
        - timestamp: timestamp
Troubleshooting
Connection issues: Check internet/API keys

Module errors: Reinstall requirements

Firebase errors: Verify Firestore rules

Dependencies
Flask

google-generativeai

firebase-admin

python-dotenv

License
MIT


To use:
1. Copy this entire text block
2. Create a new file named `README.md` in your project
3. Paste the content
4. Replace placeholder values (like GitHub URL and API key instructions)
5. Save the file

The formatting will be preserved when viewed on GitHub or other Markdown viewers.
