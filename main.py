from news_scraper import scrape_articles
from scrape_newspage import build_list_of_articles
from create_tweet import handle_articles_list
from post_tweet import tweet

def main():
    topic = "German Bundesliga Transfer News"
    print("Scraping articles...")
    articles = scrape_articles(topic, 5)
    articles = build_list_of_articles(articles)
    print("Creating tweet...")
    to_post = handle_articles_list(articles, "⚽️ Bundesliga Transfer News ⚽️")
    print(to_post)
    print("Posting tweet...")
    tweet(to_post)

    # TODO: Add IFTTT and Webhook functionality to automate bot

main()

