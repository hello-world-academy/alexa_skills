# Building an Alexa skill

This repository showcases how to develop an Alexa skill. For the purpose of demonstration __we build a skill that accesses the [Hacker News website](https://thehackernews.com/) via the [Hacker News API](https://github.com/HackerNews/API) and parses the top 10 stories listed at the time and makes an Echo device read them out loud__. 

The workflow is inspired by the video series by Harrison Kinsley (part [1](https://pythonprogramming.net/intro-alexa-skill-flask-ask-python-tutorial/), [2](https://pythonprogramming.net/headlines-function-alexa-skill-flask-ask-python-tutorial/?completed=/intro-alexa-skill-flask-ask-python-tutorial/), [3](https://pythonprogramming.net/testing-deploying-alexa-skill-flask-ask-python-tutorial/?completed=/headlines-function-alexa-skill-flask-ask-python-tutorial/)) and the [blog post](https://blog.craftworkz.co/flask-ask-a-tutorial-on-a-simple-and-easy-way-to-build-complex-alexa-skills-426a6b3ff8bc) by Bjorn Vuylsteker. 

## Requirements

You need...
* an [Amazon Echo device](https://en.wikipedia.org/wiki/Amazon_Echo) (either an Amazon Echo, Amazon Echo Plus or Amazon Echo Dot).
* an [Amazon Developer account](https://developer.amazon.com/com/)
* (recommended) the [Amazon Alexa app](https://en.wikipedia.org/wiki/Amazon_Alexa#App)

Further we need some software tools...

* a [Python](https://www.python.org/) installation  (tested on $\geq 3.6$)
* [Flask-Ask](https://github.com/johnwheeler/flask-ask)
* [requests](http://docs.python-requests.org/en/master/) 
* (recommended) [Ngrok](https://ngrok.com/)

## Getting started

The workflow consists of three main steps:

1. Build the data retrieval system
2. Build a web app 
3. Build the Alexa skill

## 1 - Data retrieval system

In this part we build the functionality to access and parse data from the [Hacker News website](https://thehackernews.com/). Therefore, we use Python and in particular the `requests` and the `json` module. 

> Create an empty Python file, named `alexa_app.py`. 

We start by importing the modules of interest:

    import json
    import requests

We further make use of the [Hacker News API](https://github.com/HackerNews/API), which provides an interface to retrieve the ids (basically just a number, associated with a particular item in the Hacker News database) of the top stories on the site at the time of query:   

    https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty

If you follow the link above you see that we get in return a [json](https://www.json.org/) structure, ranking a number of items. Being aware of the data representation we can write a Python function, called `get_top_stories`, to retrieve a specified number of entries:   

    def get_top_stories(top=10):
        sess = requests.Session()
        url = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'
        html = sess.get(url)
        ids = json.loads(html.content.decode('utf-8'))
        ids = ids[:top]
        return ids

Once we extracted the item ids, we may use another call of the Hacker News API to extract additional information, among others the title or the url of the referenced item, with respect to a particular id:

    https://hacker-news.firebaseio.com/v0/item/8863.json?print=pretty

The link above provides additional information for the item with the id of `8863`. In the nexte step we write a Python function, called `get_item_dict`,  to read the additional information for any given number of ids and store them into a Python dictionary, which is a data structure made of  a set of `key : value` pairs.

    def get_item_dict(ids):
        item_dict = {}
        sess = requests.Session()
        for item in ids:
            url = 'https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'.format(item)
            html = sess.get(url)
            item_data = json.loads(html.content.decode('utf-8'))
            item_dict[item] = item_data
        return item_dict

For the purpose of this showcase we are only interested in the titles of the selected items, hence we write one more Python function, called `process_info`, to extract the titles of items organized in form of a Python dictionary, and puts these titles into a string object.  

    def process_info(item_dict):
        titles = []
        for key in item_dict.keys():
            titles.append(item_dict[key].get('title'))
        item_info = "... ".join([x for x in titles])
        return item_info

Well, we are done! The only thing left is to write another function, called `get_headlines`, which simply calls all the functions we have written so far in a particular order.

    def get_headlines():
        top_stories_ids = get_top_stories()
        item_dict = get_item_dict(top_storiesids)
        data = process_info(item_dict)
        return data

The result of the `get_headlines` function will be a simple character string object, hence plain text, of the ten top stories on the Hacker News website at the time of query. 

## 2 - Build a web app 

    app = Flask(__name__)
    ask = Ask(app, "/hacker_news_reader")

    @app.route('/')
    def homepage():
        return "Welcome to the Hacker News Reader, an Alexa app to get the top trending stories in the digital sphere."

    if __name__ == '__main__':
        app.run(debug=True)

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