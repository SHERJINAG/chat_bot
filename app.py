from flask import Flask, render_template, request, jsonify
import nltk
import wikipedia
import pyjokes
import re

app = Flask(__name__)

# NLTK for basic natural language processing
nltk.download('punkt')

# Function to fetch data from Wikipedia
def fetch_from_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        return "I'm sorry, I found multiple results. Please be more specific."
    except wikipedia.exceptions.PageError as e:
        return "I couldn't find any information on that topic."

# Chatbot responses
chatbot_responses = [
    (r'hi|hello|hey', ['Hello!', 'Hi there!', 'Hey!']),
    (r'how are you?', ['I am just a computer program, so I don\'t have feelings, but I\'m here to help!']),
    (r'what is your name?', ['I am a chatbot. You can call me ChatBot.']),
    (r'bye|goodbye', ['Goodbye!', 'See you later!', 'Have a great day!']),
    (r'tell me a joke', [pyjokes.get_joke()]),
    (r'tell me about (.*)', [None]),
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    matched_response = None

    for pattern, responses in chatbot_responses:
        match = re.match(pattern, user_input.lower())
        if match:
            if responses[0] is None:
                # Handle Wikipedia query
                query = match.group(1)
                matched_response = fetch_from_wikipedia(query)
            else:
                matched_response = responses

    if matched_response:
        if isinstance(matched_response, list):
            if matched_response[0] is None:
                response = "Please wait while I fetch data from Wikipedia..."
            else:
                response = matched_response[0]
        else:
            response = matched_response
    else:
        response = "I'm sorry, I don't know how to respond to that."

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
