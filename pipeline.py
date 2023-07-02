from news_scraper import scrape_articles
from scrape_newspage import build_list_of_articles
from create_tweet import handle_articles_list
from post_tweet import tweet

def scrape_and_tweet(topic: str, title: str, num_articles: int) -> None:
    articles = scrape_articles(topic, num_articles)
    articles = build_list_of_articles(articles)
    to_post = handle_articles_list(articles, title)
    tweet(to_post)