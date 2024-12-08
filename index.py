import requests
import json

# OpenAI API Configuration
OPENAI_API_KEY = ""
OPENAI_API_BASE_URL = ""

# Function to send user input to OpenAI's ChatGPT API using HTTP requests
def chat_with_openai(user_input):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ],
    }

    try:
        response = requests.post(OPENAI_API_BASE_URL, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for HTTP issues
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Main handler to process and return responses in a structured format
def handler(event, context):
    """
    Entry-point for Serverless Function.
    :param event: Request payload containing user input.
    :param context: Execution context (optional).
    :return: JSON-like response with the AI's answer.
    """
    user_input = event.get("request", {}).get("original_utterance", "").strip()

    if not user_input:
        return {
            "version": event.get("version", "1.0"),
            "session": event.get("session", {}),
            "response": {
                "text": "Пожалуйста, введите запрос.",
                "end_session": False,
            },
        }
    
    if user_input.lower() in ["выход", "exit"]:
        return {
            "version": event.get("version", "1.0"),
            "session": event.get("session", {}),
            "response": {
                "text": "До свидания!",
                "end_session": True,
            },
        }

    # Get response from OpenAI
    openai_response = chat_with_openai(user_input)

    return {
        "version": event.get("version", "1.0"),
        "session": event.get("session", {}),
        "response": {
            "text": openai_response,
            "end_session": False,
        },
    }
