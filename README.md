
<div align="center">
<img alt="Logo" src="https://github.com/arnavmarda/twitter-news-bot/blob/main/docs/logo.png" width=200 />
</div>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/twitternewsbot.svg)](https://badge.fury.io/py/twitternewsbot)

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

</div>

# twitter-news-bot

A python API allowing users to:

1. Scrape news articles from Google News.
2. Extract the articles from the news sources.
3. Create and post tweets(or now Xs) using `tweepy`.
4. Leverage PaLM to generate summaries from articles as tweets and to generate tweets.
5. Pipeline and automate the scraping and tweeting procedure using a `cron` job.

# Quick Start
For complete documentation and examples, please refer to the [documentation](https://arnavmarda.github.io/twitter-news-bot/).

## Installation
```bash
pip install twitternewsbot
```

## Requirements - before using the API
For more information on how to generate the following keys and tokens, please refer to the [documentation](https://arnavmarda.github.io/twitter-news-bot/).

1. To use the `tweepy` API to post tweets, you must have a Twitter developer account and create an app. You can create an app [here](https://developer.twitter.com/en/apps). Don't worry, Twitter gives you 1 free app. Once you have created an app, you will need to generate the following keys and tokens:
    - Consumer API key
    - Consumer API secret key
    - Access token
    - Access token secret

2. To use PaLM to generate tweets and completely automate the process, you will need to generate a PaLM API. To get this, you will need to sign up for the waitlist [here](https://makersuite.google.com/waitlist). You can then generate the API key.

These keys must be stored in a `.env` file in the root directory of your project. The `.env` file should look like this:
```bash
API_KEY="your-key-here"
API_SECRET_KEY="your-key-here"
ACCESS_TOKEN="your-key-here"
ACCESS_TOKEN_SECRET="your-key-here"
GOOGLE_API_KEY="your-key-here"
```

## Usage
The API is very simple to use. Here is a quick example:
```python
from twitter_news_bot.tweeter import Tweeter
from twitter_news_bot.newsfinder import NewsFinder
from twitter_news_bot.twitternewsbot import TwitterNewsBot

# Create a NewsFinder and Tweeter Object
nf = NewsFinder()
t = Tweeter()

# Create a TwitterNewsBot object
tnb = TwitterNewsBot(nf, t, topic="AI")

# Run the TwitterNewsBOt to scrape articles, extract them, summarize them and post them as tweets
tnb.run()
```

# Future Updates
- Add support for other summarization models such as OpenAI.
- Add region based searching for news articles on Google News.
