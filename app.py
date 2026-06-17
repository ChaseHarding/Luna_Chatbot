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
stemmer = PorterStemmer

