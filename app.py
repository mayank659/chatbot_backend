from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv(dotenv_path=r"D:\react\chatbot_backend\.env")


app=Flask(__name__)
CORS(app,origins=["https://my-chatbot-one-flame.vercel.app","http://localhost:5173"])


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


   
@app.route("/")
def home():
    return "Backend Running!"

chat_history = []
@app.route('/chat', methods=['POST'])
def chat():
 try:
    message = request.json.get('message')
    chat_history.append({
       "role": "user",
       "content": message
    })
    conversation = ""
    date = datetime.now()
 
    for msg in chat_history:
        if msg['role'] == 'user':
            conversation += f"User: {msg['content']}\n"
        elif msg['role'] == 'assistant':
            conversation += f"AI: {msg['content']}\n"
    response = client.models.generate_content(
        model="gemma-4-31b-it",
        contents=f"""
You are Maya, an AI assistant built by Mayank.

Rules:
- If someone asks your name, say: "My name is Maya."
- If someone asks who created or built you, say: "I was built by Mayank."
- Answer normally for other questions.

Conversation:
{conversation}
Time:
{date}
"""
    )

    chat_history.append({
        "role": "assistant",
        "content": response.text
    })
    
    return jsonify({'response': response.text})
 except Exception as e:
     print(f"Error: {str(e)}")
     return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

print(app.url_map)    