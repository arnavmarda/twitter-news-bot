from news_scraper import scrape_articles
from scrape_newspage import build_list_of_articles
from create_tweet import handle_articles_list
from post_tweet import tweet

def scrape_and_tweet(topic: str, title: str, num_articles: int) -> None:
    print("Scraping...")
    articles = scrape_articles(topic, num_articles)
    print("Building list of articles...")
    articles = build_list_of_articles(articles)
    print("Creating tweet...")
    to_post = handle_articles_list(articles, title)
    print("Tweeting...")
    tweet(to_post)