# opeani_conversation_sqlite
Here is the conversation is stored in sql lite and trained to the that data with model thorough the help of the lang chain 

# Conversational AI with SQLite, Flask, and LangChain

This project is a conversational AI system that stores conversation data in an SQLite database and leverages OpenAI's GPT-4 for generating responses. The system is built using Flask for creating a web API, SQLite for data storage, and LangChain for handling message history and integration with the language model.

## Features

- **SQLite Database:** Lightweight and serverless database for storing conversation data.
- **Flask API:** RESTful API for interacting with the AI model.
- **OpenAI GPT-4:** Advanced natural language processing for generating intelligent responses.
- **LangChain:** Manages conversation history and integrates with the OpenAI API.

## Requirements

- Python 3.8+
- Flask
- OpenAI API key
- SQLite

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/conversational-ai.git
    cd conversational-ai
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up your OpenAI API key:

    ```bash
    export OPENAI_API_KEY='your-openai-api-key'
    ```

5. Create the SQLite database:

    ```bash
    sqlite3 sqlite.db < schema.sql
    ```

## Usage

1. Run the Flask application:

    ```bash
    flask run
    ```

2. Send a POST request to the `/query` endpoint with a JSON payload containing the `message` and `session_id`. If `session_id` is `0`, a new session will be created. For example:

    ```bash
    curl -X POST http://127.0.0.1:5000/query -H "Content-Type: application/json" -d '{"message": "Hello!", "session_id": "0"}'
    ```

## Endpoint

### `/query` (POST)

#### Request

- **Body:**
    - `message` (string): The user's message.
    - `session_id` (string): The session ID. If `0`, a new session will be created.

#### Response

- **200 OK:**
    - `response` (string): The AI's response.
    - `session_id` (string): The session ID.
- **500 Internal Server Error:**
    - `error` (string): The error message.

## Code Explanation

```python
import json
import os
import uuid
from flask import Flask, request, jsonify
from openai import OpenAI
from langchain_community.chat_message_histories import SQLChatMessageHistory

app = Flask(__name__)

connection_string = "sqlite:///sqlite.db"

os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
client = OpenAI()

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    user_message = data.get('message', '')
    session_id = data.get("session_id", '0')  

    if session_id == '0':
        session_id = str(uuid.uuid4())

    chat_message_history = SQLChatMessageHistory(
        session_id=session_id, connection_string=connection_string
    )

    if user_message == "clear":
        res = chat_message_history.clear_messages(session_id)
        if res:
            return jsonify({"message": "Session history cleared."}), 200

    messages = [
        {"role": "system", "content": "You are an intelligent assistant."},
        {"role": "user", "content": f"This is your conversation history: {chat_message_history.messages}"},
        {"role": "user", "content": user_message}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4",
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
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
