from flask import Flask, request
from pipeline import scrape_and_tweet

app = Flask(__name__)

@app.route('/', methods=['GET'])
def landing():
    return 'Hello World!'

@app.route('/tweet', methods=['GET'])
def tweet():

    print("Tweeting...")
    
    # English PL Tweet
    scrape_and_tweet("English Premier League Transfer News", "⚽️ PL Transfer News ⚽️", 5)

    # # Spanish La Liga Tweet
    # scrape_and_tweet("Spanish La Liga Transfer News", "⚽️ La Liga Transfer News ⚽️", 5)

    # # German Bundesliga Tweet
    # scrape_and_tweet("German Bundesliga Transfer News", "⚽️ Bundesliga Transfer News ⚽️", 5)

    # # Italian Serie A Tweet
    # scrape_and_tweet("Italian Serie A Transfer News", "⚽️ Serie A Transfer News ⚽️", 5)

    # # French Ligue 1 Tweet
    # scrape_and_tweet("French Ligue 1 Transfer News", "⚽️ Ligue 1 Transfer News ⚽️", 5)

    # # NBA Tweet
    # scrape_and_tweet("NBA Trade News and Rumors", "🏀 NBA Trade News 🏀", 5)

    return 'Tweeted!'

if __name__ == '__main__':
    app.run(host="0.0.0.0")