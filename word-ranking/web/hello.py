from bs4 import BeautifulSoup
from collections import defaultdict
from flask import Flask
from flask import request
from flask import jsonify
from .db import create_tables
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/topwords', methods = ['GET'])
def top_words():
    # to do: add parameter error checking
    url = request.args['url']
    limit = int(request.args['limit'])
    words = get_top_words_from_url(url, limit)
    return jsonify(words)

def get_top_words_from_url(url, limit):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.find_all(text=True)

    words_dict = defaultdict(int)
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head',
        'input',
        'script',
    ]

    for t in text:
        if t.parent.name not in blacklist:
            words = t.split()
            for word in words:
                if word.isalnum():
                    words_dict[word.lower()] += 1

    sorted_words = sorted(words_dict.items(),
                          key=lambda a:a[1],
                          reverse=True
                         )[:limit]

    sorted_words_object = []
    for word, count in sorted_words:
        sorted_words_object.append({word: count})
    return sorted_words_object
