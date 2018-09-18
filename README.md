# Building an Alexa skill

This repository showcases how to develop an Alexa skill. For the purpose of demonstration __we build a skill that accesses the [Hacker News website](https://thehackernews.com/) via the [Hacker News API](https://github.com/HackerNews/API) and parses the top 10 stories listed at the time and makes an Echo device read them out loud__. 

The workflow is inspired by the video series by Harrison Kinsley (part [1](https://pythonprogramming.net/intro-alexa-skill-flask-ask-python-tutorial/), [2](https://pythonprogramming.net/headlines-function-alexa-skill-flask-ask-python-tutorial/?completed=/intro-alexa-skill-flask-ask-python-tutorial/), [3](https://pythonprogramming.net/testing-deploying-alexa-skill-flask-ask-python-tutorial/?completed=/headlines-function-alexa-skill-flask-ask-python-tutorial/)) and the [blog post](https://blog.craftworkz.co/flask-ask-a-tutorial-on-a-simple-and-easy-way-to-build-complex-alexa-skills-426a6b3ff8bc) by Bjorn Vuylsteker. 

## i) Requirements

You need...
* an [Amazon Echo device](https://en.wikipedia.org/wiki/Amazon_Echo) (either an Amazon Echo, Amazon Echo Plus or Amazon Echo Dot).
* an [Amazon Developer account](https://developer.amazon.com/com/)
* (recommended) the [Amazon Alexa app](https://en.wikipedia.org/wiki/Amazon_Alexa#App)

Further we need some software tools...

* a [Python](https://www.python.org/) installation  (tested on $\geq 3.6$)
* [Flask-Ask](https://github.com/johnwheeler/flask-ask)
* [requests](http://docs.python-requests.org/en/master/) 
* (recommended) [Ngrok](https://ngrok.com/)

## ii) Getting started

The workflow consits of three main steps:
1. Build the data retrieval system
2. Build a web app 
3. Build the Alexa skill

## 1 - Data retrieval system

In this part we build the functionallity to access and parse data from the [Hacker News website](https://thehackernews.com/). Therefore, we use Python and in particular the `requests` and the `json` module. 

> Create an empty Python file, named `alexa_app.py`. 

We start by importing the modules of interest:

    import json
    import requests


We further make use of the [Hacker News API](https://github.com/HackerNews/API), which allows us the retrieve the item ids of 


    def get_top_stories(top=10):
        '''
        A function to retrieve item ids of the top stories listed on HacherNews.com
        '''
        sess = requests.Session()
        url = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'
        html = sess.get(url)
        data = json.loads(html.content.decode('utf-8'))
        data = data[:top]
        return data

    def get_item_dict(data):
        item_dict = {}
        sess = requests.Session()
        for item in data:
            url = 'https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'.format(item)
            html = sess.get(url)
            item_data = json.loads(html.content.decode('utf-8'))
            item_dict[item] = item_data
        return item_dict

    def process_info(d):
        titles = []
        for key in d.keys():
            titles.append(d[key].get('title'))
        item_info = "... ".join([x for x in titles])
        return item_info

def get_headlines():
    top_stories = get_top_stories()
    item_dict = get_item_dict(top_stories)
    data = process_info(item_dict)
    return data