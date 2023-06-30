from requests_html import HTMLSession
import requests

def scrape_news_article(url):

    # Final url
    try:
        url = requests.get(url, timeout=5).url
    except Exception as error:
        print(f"Error: {error} for url: {url}")
        return None

    # Initialize HTML Session
    session = HTMLSession()

    # Get the page
    r = session.get(url=url)

    title  = r.html.find('h1', first=True).text

    # Get all article fragments (each fragment is a paragraph)
    article_fragments = r.html.find('p')

    # Join all the paragraphs to form the article
    article_fragments_all = '\n'.join([fragment.text for fragment in article_fragments])

    return {'title': title, 'article': article_fragments_all} 

def build_article_from_dict(article_dict):
    return scrape_news_article(article_dict['link'])

def build_list_of_articles(articles_list):
    articles_full_text = []
    for article in articles_list:
        article_text = build_article_from_dict(article)
        if article_text is not None:
            articles_full_text.append(article_text)
    return articles_full_text