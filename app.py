from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=r"D:\react\chatbot_backend\.env")


app=Flask(__name__)
CORS(app)


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

    for msg in chat_history:
        if msg['role'] == 'user':
            conversation += f"User: {msg['content']}\n"
        elif msg['role'] == 'assistant':
            conversation += f"AI: {msg['content']}\n"
    response = client.models.generate_content(
        model="gemma-4-31b-it",
        contents=conversation
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