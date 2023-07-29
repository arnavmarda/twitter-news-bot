# Installation

## Installing the package
The fastest and easiest way to install the package is using `pip`:
```bash
pip install twitternewsbot
```
The `pip` package usually comes installed with python but if you do not have it, you can install it from [here](https://pip.pypa.io/en/stable/installation/).

You can also install the package by downloading the source code available [here](https://github.com/arnavmarda/twitter-news-bot/archive/refs/tags/v2.0.zip).

Moreover, you can also `git clone` the repository:
```bash
git clone https://github.com/arnavmarda/twitter-news-bot.git
```

## Setting up the .env file

**Note - This step is optional. You can also pass the keys and tokens directly to the API. This will not work for the `pip` installation.**

twitter-news-bot uses the `tweepy` API to post tweets and leverages Google PaLM to generate summaries and tweets. To use these APIs, you will need to generate keys and tokens.

These keys and tokens are stored and read from the `.env` file in the root directory of your project.

You can create the file using your IDE or file explorer or simply running the following command in the root directory of your project:
```bash
touch .env
```

The API keys must be stored in the `.env` file as such:
```bash
API_KEY="your-key-here"
API_SECRET_KEY="your-key-here"
ACCESS_TOKEN="your-key-here"
ACCESS_TOKEN_SECRET="your-key-here"
GOOGLE_API_KEY="your-key-here"
```

## Getting the API keys and tokens
1. To use the `tweepy` API to post tweets, you must have a Twitter developer account and create an app. You can create an app [here](https://developer.twitter.com/en/apps). Don't worry, Twitter gives you 1 free app. Once you have created an app, you will need to generate the following keys and tokens:
    - Consumer API key
    - Consumer API secret key
    - Access token
    - Access token secret

2. To use PaLM to generate tweets and completely automate the process, you will need to generate a PaLM API. To get this, you will need to sign up for the waitlist [here](https://makersuite.google.com/waitlist). You can then generate the API key.

## Package Requirements
If you are using the `pip` installation, you do not need to worry about the package requirements. However, if you are using the source code, you will need to install the following packages by running:
```bash
pip install -r requirements.txt
```
The tech stack used in this project includes the following open-source libraries:
- [tweepy](https://www.tweepy.org/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [requests](https://pypi.org/project/requests/)
- [requests-html](https://pypi.org/project/requests-html/)
- [validators](https://pypi.org/project/validators/)
- [cron-validator](https://pypi.org/project/cron-validator/)
- [google-generativeai](https://github.com/google/generative-ai-python)