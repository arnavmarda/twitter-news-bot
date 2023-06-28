from requests_html import HTMLSession
import re

def scrape_articles(topic):
    """

    Scrape the news articles from Google News for a given topic

    Parameters
    ----------
    topic : str
        The topic to search for

    Returns
    -------
    all_articles : list
        A list of dictionaries containing the title, source, time and link of each article
    """

    # Initialize an HTML Session
    session = HTMLSession()

    # Initalize URL
    query = topic.replace(' ', '+')
    url = f'https://news.google.com/search?for={query}&hl=en-GB&gl=GB&ceid=GB:en'

    # Get the page
    r = session.get(url=url)

    # print(r.html.find('article', first=True).find('h3', first=True).text)    
    # print(r.html.find('article', first=True).find('img', first=True).attrs.get('alt'))
    # print(r.html.find('article', first=True).find('time', first=True).text)

    # Get all the articles
    articles = r.html.find('article')
    all_articles = []

    # Iterate over each article
    for article in articles:
        # Get the title
        title = article.find('h3', first=True).text

        # Get the source
        source = article.find('img', first=True).attrs.get('alt')

        # Get the time
        time = article.find('time', first=True).text
        numbersRegex = re.compile(r'\d+')
        unitRegex = re.compile(r'hour|day|minute|Yesterday')
        unit = unitRegex.findall(time)
        if unit == []:
            continue
        unit = unit[0]
        if unit == 'Yesterday':
            continue
        
        numbers = numbersRegex.findall(time)[0]
        

        if (int(numbers) > 12 and unit == 'hour') or (unit == 'day') or (unit == 'Yesterday'):
            continue

        # Get the link
        link = article.find('a', first=True).attrs['href']

        # Print the details
        newsarticle = {
            'title': title,
            'source': source,
            'time': time,
            'link': link
        }
        all_articles.append(newsarticle)

    return all_articles

print(help(scrape_articles))
    
    
# if __name__ == '__main__':
#     main()