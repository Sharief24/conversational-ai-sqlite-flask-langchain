import json
import os
import uuid
from flask import Flask, request, jsonify
from openai import OpenAI
from langchain_community.chat_message_histories import SQLChatMessageHistory
 
app = Flask(__name__)
 
connection_string="sqlite:///sqlite.db"

os.environ["OPENAI_API_KEY"] = "your_api_key"
client = OpenAI()
 
@app.route('/query', methods=['POST'])
def query():
    data= request.get_json()
    user_message = data.get('message', '')
    session_id = data.get("session_id",'0')  

    if session_id == '0':
        session_id = str(uuid.uuid4())

    chat_message_history = SQLChatMessageHistory(
    session_id=session_id, connection_string=connection_string
    )

    #clear session history
    if user_message=="clear":
        res =chat_message_history.clear_messages(session_id)
        if res:
            return jsonify({"message": "Session history cleared."}), 200
  
 
    messages = [
        {"role": "system", "content": "You are an intelligent assistant."},
        {"role":"user","content": f"This is you are conversation history:{chat_message_history.messages}"},
        {"role": "user", "content": user_message}
    ]
 
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            seed=42,
            temperature=0.000001
        )       
        bot_response = response.choices[0].message.content
        if bot_response:
            chat_message_history.add_user_message(user_message)
            chat_message_history.add_ai_message(bot_response)
        return jsonify({"response": bot_response, "session_id": session_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
if __name__ == '__main__':
    app.run(debug=True)