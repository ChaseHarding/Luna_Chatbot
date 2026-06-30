from flask import Flask, request, jsonify, render_template
from datetime import datetime 
import json 
import random 
import re 
import os
import nltk
from nltk.stem import PorterStemmer

# pre trained model splits sentences and quiet=True will prevent any unecessary printing to the terminal when downloading
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

app = Flask(__name__)
#reduces word to its root so LUNA can understand users easier 
stemmer = PorterStemmer()

#loading the intents 
with open('intents.json') as f:
    data = json.load(f)

# In-memory conversation storage
# key = session_id, value = list of past messages
conversation_history = []

def tokenize(text):
    return nltk.word_tokenize(text.lower())

def stem(word):
    return stemmer.stem(word.lower())

#matching the logic 
def get_intent(message):

    #detect math expressions without the pattern words present
    math_pattern = r'-?\d+(?:\.\d+)?\s*[+\-*/^%]\s*-?\d+(?:\.\d+)?'
    if re.search(math_pattern, message):
        for intent in data['intents']:
            if intent['tag'] == 'math':
                return intent

    message_words = [stem(w) for w in tokenize(message)]
    best_match = None 
    best_score = 0
#look through each intnent
    for intent in data['intents']:
        #look through each pattern of the intent 
        for pattern in intent['patterns']:
            pattern_words = [stem(w) for w in tokenize(pattern)]
            #count how many pattern words appear in the message 
            matches = sum(1 for w in pattern_words if w in message_words)
            #divide matches by total number of pattern words for a percentage
            score = matches / len(pattern_words) if pattern_words else 0
            #Example: user says 'tell me a joke', pattern is 'tell me a joke'
            #pattern_words = 'tell' 'me' 'a' 'joke'
            #matches = 4
            #score = 4/4 1.0 (perfect match)
            if score > best_score:
                best_score = score
                best_match = intent

    if best_score > 0.5:
        return best_match
    return None

#handling dynamic messages: ie. time/date/math
def handle_dynamic(tag, message):
    if tag == 'coin_flip':
        result = random.choice(['Heads', 'Tails'])
        return f"🪙 {result}!"
    if tag == 'roll_die':
        result = random.randint(1, 6)
        return f"🎲 You rolled a {result}!"
    if tag == 'time':
        return f"The current time is {datetime.now().strftime('%I:%M %p')}."
    if tag == 'date':
        return f"Today is {datetime.now().strftime('%A, %B, %d, %Y')}."
    if tag == 'math':
        try:
            cleaned = message.lower()

            cleaned = cleaned.replace('divided by', '/')
            cleaned = cleaned.replace('times', '*')
            cleaned = cleaned.replace('plus', '+')
            cleaned = cleaned.replace('minus', '-')
            cleaned = cleaned.replace('squared', '**2')
            cleaned = cleaned.replace('cubed', '**3')
            cleaned = cleaned.replace('^', '**')
            print(f"After ^ replace: {cleaned}")
            cleaned = re.sub(r'\bx\b', '*', cleaned)
            cleaned = re.sub(r'sqrt\s*\(?\s*(\d+)\s*\)?', r'math_module.sqrt(\1)', cleaned)

            expression = re.sub(r'[^0-9+\-*/().%\s]', '', cleaned)

            print(f"Evaluating: {expression}")

            result = eval(expression)
            return f"The result is {result}."
        
        except ZeroDivisionError:
            return "You can't divide by zero, silly."
        except Exception:
            return "I couldn't calculate that. Try something like '5 + 3'."
    if tag == 'recall_last':
        user_messages = [m for m in conversation_history if m['role'] == 'user']
        if len(user_messages) >= 2:
            last_user_message = user_messages[-2]['content']
            return f"You just said: \"{last_user_message}\""
        return "You haven't said anything yet!"
    return None

# actual web server wow
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    body = request.get_json()
    message = body.get('message', '')

    #storing conversation history per session
    conversation_history.append({'role': 'user', 'content': message})

    intent = get_intent(message)

    if intent:
        dynamic = handle_dynamic(intent['tag'], message)
        if dynamic: 
            response = dynamic
        else: 
            response = random.choice(intent['responses'])
    else:
            fallback_intent = None
            for i in data['intents']:
                if i ['tag'] == 'fallback':
                    fallback_intent = i
                    break
            response = random.choice(fallback_intent['responses'])
    conversation_history.append({"role": "bot", "content": response})
    return jsonify({'response': response})

@app.route('/history')
def history():
    return jsonify(conversation_history)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)