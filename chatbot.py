import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Verify API key is loaded
if not API_KEY:
    raise ValueError("No GOOGLE_API_KEY found in environment variables. Please check your .env file")

# Configure Google AI Studio
try:
    genai.configure(api_key=API_KEY)
    print("Google Gemini API configured successfully")
except Exception as e:
    print(f"Error configuring Gemini API: {str(e)}")
    raise

# Initialize Firebase (if using)
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase initialized successfully")
except Exception as e:
    print(f"Firebase initialization error: {str(e)}")
    db = None  # Continue without Firebase if it fails

app = Flask(__name__)

def chat_with_ai(user_input, conversation_id=None):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_input)
        ai_response = response.text
        
        # Store the conversation in Firebase if db is available
        if db and conversation_id:
            try:
                # Add the message to the conversation
                messages_ref = db.collection('conversations').document(conversation_id).collection('messages')
                messages_ref.add({
                    'user_input': user_input,
                    'ai_response': ai_response,
                    'timestamp': datetime.now()
                })
                
                # Update the conversation's last updated time
                db.collection('conversations').document(conversation_id).update({
                    'updated_at': datetime.now()
                })
            except Exception as e:
                print(f"Firebase storage error: {str(e)}")
        
        return ai_response
    except Exception as e:
        print(f"Error generating content: {str(e)}")
        return "Sorry, I encountered an error processing your request."

@app.route('/')
def home():
    conversation_id = "local-session"  # Default if not using Firebase
    if db:
        try:
            conversation_ref = db.collection('conversations').document()
            conversation_ref.set({
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            })
            conversation_id = conversation_ref.id
        except Exception as e:
            print(f"Firebase error: {str(e)}")
    
    return render_template('chat.html', conversation_id=conversation_id)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    conversation_id = request.form.get('conversation_id', 'local-session')
    
    response = chat_with_ai(user_input, conversation_id)
    
    return jsonify({
        'response': response,
        'conversation_id': conversation_id
    })

if __name__ == '__main__':
    app.run(debug=True)