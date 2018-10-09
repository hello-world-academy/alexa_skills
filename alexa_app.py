from flask import Flask
from flask_ask import Ask, statement, question
import json
import requests

# helper functions for API data stream
def get_top_stories(top=10):
    sess = requests.Session()
    url = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'
    html = sess.get(url)
    ids = json.loads(html.content.decode('utf-8'))
    ids = ids[:top]
    return ids

def get_item_dict(ids):
    item_dict = {}
    sess = requests.Session()
    for item in ids:
        url = 'https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'.format(item)
        html = sess.get(url)
        item_data = json.loads(html.content.decode('utf-8'))
        item_dict[item] = item_data
    return item_dict

def process_info(item_dict):
    titles = []
    for key in item_dict.keys():
        titles.append(item_dict[key].get('title'))
    item_info = "... ".join([x for x in titles])
    return item_info

def get_headlines():
    top_stories_ids = get_top_stories()
    item_dict = get_item_dict(top_stories_ids)
    data = process_info(item_dict)
    return data

# Building an app
app = Flask(__name__)
ask = Ask(app, "/hacker_news_reader")

@app.route('/')
def homepage():
    return "Welcome to my Alexa app."

@ask.launch
def start_skill():
    welcome_message = 'Hello there, would you like the top stories of hacker news?'
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
    headlines = get_headlines()
    headline_msg = 'The current hacker news top stories headlines are {}'.format(headlines)
    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'I am not sure why you asked me to run then, but okay... bye'
    return statement(bye_text)

if __name__ == '__main__':
    app.run(debug=True)