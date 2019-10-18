from flask import Flask
from flask import request
from flask import jsonify
from bs4 import BeautifulSoup
import requests
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/topwords', methods = ['GET'])
def top_words():
    # to do: add error checking
    url = request.args['url']
    words = get_words_from_url(url)
    return jsonify(words)

def get_words_from_url(url):
    response = requests.get(url)
    html = response.text
    words = ['word1', 'word2']
    return words
