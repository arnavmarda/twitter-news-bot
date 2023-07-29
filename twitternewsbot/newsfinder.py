# Import statements
from requests_html import HTMLSession
import requests
import warnings
from validators.domain import domain
import sys

class NewsFinder():

    """
    API Object to scrape news articles from Google News and scrape the article text from the news website. 
    Allows filtering of Google News results.

    Note: Due to issues with scraping, Daily Mail and News18 are blocked by default. You can unblock them by calling the remove_blocked_source method but this is not advised.

    Attributes
    ----------
    blocked_sources : list
        A list of sources to block, by default includes Daily Mail and News18
    """

    #####################################
    # Initialization
    #####################################

    def __init__(self, blocked_sources: list|None = None):
        """Initialize the NewsFinder class
        
        Parameters
        ----------
        blocked_sources : list, optional
            A list of sources to block, by default includes Daily Mail and News18        

        Raises
        ------
        TypeError
            If blocked_sources is not a list
        TypeError
            If any element in blocked_sources is not a string    
        """

        if blocked_sources is None:
            self.blocked_sources = ["Daily Mail", "News18"]
        else:

            # Check if blocked_sources is valid
            if not isinstance(blocked_sources, list):
                raise TypeError("blocked_sources must be a list")
            
            # Check if all elements in blocked_sources are strings
            if not all(isinstance(source, str) for source in blocked_sources):
                raise TypeError("blocked_sources must be a list of strings")

            self.blocked_sources = blocked_sources + ["Daily Mail", "News18"]

    #####################################
    # Private Methods
    #####################################

    def __scrape_articles(self, url: str, number_of_articles: int = 5) -> list | None:
        """Private: Scrape the news articles from Google News for a given topic

        Parameters
        ----------
        url : str
            The google news url to scrape
        number_of_articles : int, optional 
            The number of articles to scrape, by default 5

        Returns
        -------
        all_articles : list
            A list of dictionaries containing the title, source, time and link of each article
        """

        # Initialize an HTML Session
        session = HTMLSession()

        # Get the page
        r = session.get(url=url)

        # Get all the articles
        try:
            articles = r.html.find('article')
        except:
            return None
        
        all_articles = []

        # Iterate over each article
        for article in articles:
            
            # Break if we have enough articles
            if len(all_articles) == number_of_articles:
                break

            # Get the title
            title = article.find('h3', first=True).text

            # Get the source
            source = article.find('img', first=True).attrs.get('alt')

            # Disallow certain sources
            if source in self.blocked_sources:
                continue
        
            # Get the link
            link = article.find('a', first=True).absolute_links.pop()

            # Print the details
            newsarticle = {
                'title': title,
                'source': source,
                'link': link
            }
            all_articles.append(newsarticle)

        return all_articles
    
    def __scrape_news_article(self, url: str) -> dict | None:
        """Private: Scrape the news article from the given url

        Parameters
        ----------
        url : str
            The google news url of the news article
        
        Returns
        -------
        article : dict
            A dictionary containing the title and article body of the news article
        """


        # Final url
        try:
            url = requests.get(url, timeout=5).url
        except Exception as error:
            warnings.warn(f"Error processing url: {url}. Continuing without it...")
            return None

        # Initialize HTML Session
        session = HTMLSession()

        # Get the page
        r = session.get(url=url)

        # Get the title
        try:
            title  = r.html.find('h1', first=True).text
        except:
            title = ""

        # Get all article fragments (each fragment is a paragraph)
        try:
            article_fragments = r.html.find('p')
        except:
            warnings.warn(f"Article with url: {url} cannot be scraped. Continuing without it...")
            return None


        # Join all the paragraphs to form the article
        body = '\n'.join([fragment.text for fragment in article_fragments])

        return {'title': title, 'article': body}
    
    def __build_list_of_articles(self, articles_list: list) -> list:
        """Private: Build a list of articles from the given list of dictionaries
        
        Parameters
        ----------
        articles_list : list(dict)
            A list of dictionaries containing the title, source, date and link of the articles

        Returns
        -------
        articles_full_text : list
            A list of dictionaries containing the title and article body of the news articles
        """

        # Iterate through articles, and scrape each one
        for article in articles_list:
            article_text = self.__build_article_from_dict(article)
            article.update(article_text)
        return articles_list
    
    def __build_article_from_dict(self, article_dict: dict) -> dict | None:
        """Private: Build the article from the given dictionary

        Parameters
        ----------
        article_dict : dict
            A dictionary containing the title, source, date and link of the article

        Returns
        -------
        article : dict
            A dictionary containing the title and article body of the news article
        """

        return self.__scrape_news_article(article_dict['link'])
    
    def __build_url(self, topic_url: str, source_url: str, period_url: str) -> str:
        """Private: Build the url for the given topic, source and period
        
        Parameters
        ----------
        topic_url : str
            The topic to search for
        source_url : str
            The url fragment of the source to search for
        period_url : str
            The url fragment of the period to search for

        Returns 
        -------
        url : str
            The url to scrape
        """

        return f'https://news.google.com/search?q={topic_url}{source_url}{period_url}&hl=en-IN&gl=IN&ceid=IN:en'
        
    
    ###############################
    # Public Methods - API Methods
    ###############################

    def add_blocked_source(self, sources: list) -> int:
        """Add a list of sources to block

        Parameters
        ----------
        sources : list
            A list of sources to block

        Returns
        -------
        int
            The number of blocked sources

        Raises
        ------
        TypeError
            If sources is not a list

        Examples
        --------
        >>> from twitternewsbot.newsfinder import NewsFinder
        >>> nf = NewsFinder() 
        >>> nf.add_blocked_source(["BBC"]) # Add BBC to the list of blocked sources
        3
        """

        # Check if the sources is valid
        if not isinstance(sources, list):
            raise TypeError("Sources must be a list")

        # Check if the source is already blocked
        for source in sources:
            if source in self.blocked_sources:
                sources.remove(source)

        self.blocked_sources = self.blocked_sources + sources
        return len(self.blocked_sources)
    
    def remove_blocked_source(self, sources: list) -> int:
        """Remove a list of sources to block

        Parameters
        ----------
        sources : list
            A list of sources to block

        Returns
        -------
        int
            The number of blocked sources
        
        Raises
        ------
        TypeError
            If sources is not a list
        
        Examples
        --------
        >>> from twitternewsbot.newsfinder import NewsFinder
        >>> nf = NewsFinder()
        >>> nf.remove_blocked_source(["Daily Mail"]) # Remove Daily Mail from the list of blocked sources
        1
        """

        # Check if the sources is valid
        if not isinstance(sources, list):
            raise TypeError("Sources must be a list")

        for source in sources:
            self.blocked_sources.remove(source)
        return len(self.blocked_sources)
    
    def get_blocked_sources(self) -> list:
        """Get the list of blocked sources

        Returns
        -------
        list
            The list of blocked sources
        
        Examples
        --------
        >>> from twitternewsbot.newsfinder import NewsFinder
        >>> nf = NewsFinder()
        >>> nf.get_blocked_sources() # Remember, Daily Mail and News18 are blocked by default (due to issues with scraping)
        ['Daily Mail', 'News18']
        """

        return self.blocked_sources
    
    @property
    def blocked_sources(self) -> list:
        """Get the list of blocked sources

        Returns
        -------
        list
            The list of blocked sources
        
        Examples
        --------
        >>> from twitternewsbot.newsfinder import NewsFinder
        >>> nf = NewsFinder()
        >>> nf.blocked_sources # Remember, Daily Mail and News18 are blocked by default (due to issues with scraping)
        ['Daily Mail', 'News18']
        """

        return self.__blocked_sources
    
    @blocked_sources.setter
    def blocked_sources(self, sources: list) -> None:
        """Set the list of blocked sources

        Parameters
        ----------
        sources : list
            A list of sources to block
            
        Raises
        ------
        TypeError
            If sources is not a list

        Examples
        --------
        >>> from twitternewsbot.newsfinder import NewsFinder
        >>> nf = NewsFinder()
        >>> nf.blocked_sources = ["BBC"] # Set the list of blocked sources to BBC
        """

        # Check if the sources is valid
        if not isinstance(sources, list):
            raise TypeError("sources must be a list")

        self.__blocked_sources = sources

    def update_blocked_sources(self, sources: list) -> int:
        """Update the list of blocked sources by completely replacing existing blocked sources

        Parameters
        ----------
        sources : list
            A list of sources to block

        Returns
        -------
        int
            The number of blocked sources
        
        Raises
        ------
        TypeError
            If sources is not a list

        Examples
        --------
        >>> from twitternewsbot.newsfinder import NewsFinder
        >>> nf = NewsFinder()
        >>> nf.update_blocked_sources(["BBC"]) # Update the list of blocked sources to BBC
        1
        """
        # Check if the sources is valid
        if not isinstance(sources, list):
            raise TypeError("Sources must be a list")
        
        self.blocked_sources = sources
        return len(self.blocked_sources)
    
    def get_news_articles(self, topic: str|None = None, number_of_articles: int|None = None, source: str|None = None, period: str = "Any time", article_text: bool = False) -> list:
        """Get the news articles for a given topic or for a given source filtered by date
        
        Parameters
        ----------
        topic : str, optional
            The topic to search for, by default None
        number_of_articles : int, optional
            The number of articles to scrape, by default None which gives all the possible articles
        source : str, optional
            The domain for the website of the source to search for, by default None. For example, "dailymail.co.uk" or "bbc.com"
        period : list, optional
            The period to search for, by default "Any time". Period must be one of ["Any time", "Past hour", "Past 24 hours", "Past week", "Past year"]
        article_text : bool, optional
            Whether to scrape the article text or not, by default False
        
        Returns
        -------
        list
            A list of dictionaries containing the title, source, link and article body of the news articles (only if article_text is True)

        Raises
        ------
        ValueError
            If the period is not one of ["Any time", "Past hour", "Past 24 hours", "Past week", "Past year"].
        ValueError
            If the number_of_articles is not a positive integer
        TypeError
            If the topic is not a string
        TypeError
            If the source is not a string
        ValueError
            If the source is not a valid domain name
        TypeError
            If the article_text is not a boolean
        ValueError
            If the topic and source are both None

        Examples
        --------

        Retrieving all articles for a given topic in the last 24 hours without scraping.

        >>> from twitternewsbot.newsfinder import NewsFinder
        >>> nf = NewsFinder()
        >>> nf.get_news_articles(topic="Donald Trump", period="Past 24 hours")

        Retrieving all articles for a given topic in the last 24 hours and scraping the article text.

        >>> from twitternewsbot.newsfinder import NewsFinder
        >>> nf = NewsFinder()
        >>> nf.get_news_articles(topic="Donald Trump", period="Past 24 hours", article_text=True)

        Retrieving 5 articles from a given source in the last week without scraping.

        >>> from twitternewsbot.newsfinder import NewsFinder
        >>> nf = NewsFinder()
        >>> nf.get_news_articles(source="bbc.com", period="Past week", number_of_articles=5)
        """

        # Check if the period is valid
        if period not in ["Any time", "Past hour", "Past 24 hours", "Past week", "Past year"]:
            raise ValueError("period must be one of ['Any time', 'Past hour', 'Past 24 hours', 'Past week', 'Past year']")
        
        # Check if the number of articles is valid
        if number_of_articles is not None and number_of_articles <= 0:
            raise ValueError("number_of_articles must be a positive integer")
        
        # Check if the topic is valid
        if topic is not None and not isinstance(topic, str):
            raise TypeError("topic must be a string")
        
        # Check if the source is valid
        if source is not None and not isinstance(source, str):
            raise TypeError("source must be a string")

        if source is not None and not domain(source):
            raise ValueError("source must be a valid domain name")

        # Check if the article_text is valid
        if not isinstance(article_text, bool):
            raise TypeError("article_text must be a boolean")
        
        # Check if the topic and source are both None
        if topic is None and source is None:
            raise ValueError("Either or both topic and source must be provided")

        ################### Build url ######################

        # If topic is provided
        if topic is not None:
            topic_url = topic + " "
        else:
            topic_url = ""

        # If source is provided
        if source is not None:
            source_url = " site:" + source
        else:
            source_url = ""

        # If period is provided

        period_mappings = {"Any time": "",
                           "Past hour": " when:1h",
                           "Past 24 hours": " when:1d",
                           "Past week": " when:7d",
                           "Past year": " when:1y"}

        period_url = period_mappings[period]

        url = self.__build_url(topic_url, source_url, period_url)


        ################### Scrape ######################

        articles = self.__scrape_articles(url, number_of_articles)

        # Check and report if no articles found
        if articles is None:
            sys.stdout.write("No articles found. Try different parameters")
            return []
        
        
        ################### Build Articles ######################
        if article_text:
            articles = self.__build_list_of_articles(articles)

        return articles