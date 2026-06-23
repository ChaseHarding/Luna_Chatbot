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

def tokenize(text):
    return nltk.word_tokenize(text.lower())

def stem(word):
    return stemmer.stem(word.lower())

#matching the logic 
def get_intent(message):
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
    if tag == 'time':
        return f"The current time is {datetime.now().strftime('%I:%M %p')}."
    if tag == 'date':
        return f"Today is {datetime.now().strftime('%A, %B, %d, #Y')}."
    if tag == 'math':
        try:
            expression = re.sub(r'[^0-9+\-*/().\s]', '', message)
            result = eval(expression)
            return f"The result is {result}."
        except:
            return "I couldn't calculate that. Try something like '5 + 3'."
    return None