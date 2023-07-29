# Import statements
from newsfinder import NewsFinder
from tweeter import Tweeter

class TwitterNewsBot():
    """
    API Object to connect the NewsFinder and Tweeter classes to build a pipeline to automate finding, scraping and tweeting news.

    Attributes
    ----------
    news_finder : NewsFinder
        The NewsFinder object to use to find and scrape news articles
    tweeter_obj : Tweeter
        The Tweeter object to use to tweet the news articles
    topic : str
        The topic to search for news articles
    no_of_articles : int
        The number of articles to find and scrape, by default 5    
    """

    #####################################
    # Initialization
    #####################################

    def __init__(self, news_finder: NewsFinder, tweeter_obj: Tweeter, topic: str, no_of_articles: int = 5):
        """Initialize the Bot class
        
        Parameters
        ----------
        news_finder : NewsFinder
            The NewsFinder object to use to find and scrape news articles
        tweeter_obj : Tweeter
            The Tweeter object to use to tweet the news articles
        topic : str
            The topic to search for news articles
        no_of_articles : int, optional
            The number of articles to find and scrape, by default 5

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If news_finder is not a NewsFinder object
            If tweeter_obj is not a Tweeter object
            If topic is not a string
            If no_of_articles is not an integer
        """
        
        # Check if news_finder is a NewsFinder object
        if not isinstance(news_finder, NewsFinder):
            raise TypeError("news_finder must be a NewsFinder object")
        
        # Check if tweeter_obj is a Tweeter object
        if not isinstance(tweeter_obj, Tweeter):
            raise TypeError("tweeter_obj must be a Tweeter object")
        
        # Check if topic is a string
        if not isinstance(topic, str):
            raise TypeError("topic must be a string")
        
        # Check if no_of_articles is an integer
        if not isinstance(no_of_articles, int):
            raise TypeError("no_of_articles must be an integer")
        
        # Set the attributes
        self.news_finder = news_finder
        self.tweeter_obj = tweeter_obj
        self.__topic = topic
        self.__no_of_articles = no_of_articles

    #####################################
    # Private Methods
    #####################################
    
    def __build_pipeline(self, **kwargs) -> dict:
        """Private: Build the pipeline to find, scrape and tweet news articles

        Parameters
        ----------
        **kwargs : dict
            Arguments for Tweeter.tweet function excluding articles_list. See Tweeter.tweet for more details on the args. 
        
        Returns
        -------
        dict
            A dictionary containing the total character count, the number of tweets posted, and the id of the parent tweet when run
        """
        
        # Build the pipeline
        articles = self.news_finder.get_news_articles(topic=self.__topic,number_of_articles=self.__no_of_articles, article_text=True)
        return self.tweeter_obj.tweet(articles_list=articles, **kwargs)
    
    ###############################
    # Public Methods - API Methods
    ###############################

    @property
    def topic(self) -> str:
        """Returns the topic to search for news articles
        
        Returns
        -------
        str
            The topic to search for news articles

        Examples
        --------
        >>> from twitternewsbot.twitternewsbot import TwitterNewsBot
        >>> from twitternewsbot.newsfinder import NewsFinder
        >>> from twitternewsbot.tweeter import Tweeter
        >>> bot = TwitterNewsBot(NewsFinder(), Tweeter(), "Python")
        >>> bot.topic
        "Python"
        """
        return self.__topic

    @topic.setter
    def topic(self, topic: str) -> None:
        """Sets the topic to search for news articles
        
        Parameters
        ----------
        topic : str
            The topic to search for news articles

        Raises
        ------
        TypeError
            If topic is not a string

        Examples
        --------
        >>> from twitternewsbot.twitternewsbot import TwitterNewsBot
        >>> from twitternewsbot.newsfinder import NewsFinder
        >>> from twitternewsbot.tweeter import Tweeter
        >>> bot = TwitterNewsBot(NewsFinder(), Tweeter(), "Python")
        >>> bot.topic = "HTML"
        """
        # Check if topic is a string
        if not isinstance(topic, str):
            raise TypeError("topic must be a string")
        
        self.__topic = topic
        return self.__topic

    @property
    def no_of_articles(self) -> int:
        """Returns the number of articles to find and scrape
        
        Returns
        -------
        int
            The number of articles to find and scrape

        Examples
        --------
        >>> from twitternewsbot.twitternewsbot import TwitterNewsBot
        >>> from twitternewsbot.newsfinder import NewsFinder
        >>> from twitternewsbot.tweeter import Tweeter
        >>> bot = TwitterNewsBot(NewsFinder(), Tweeter(), "Python")
        >>> bot.no_of_articles
        5
        """
        return self.__no_of_articles
    
    @no_of_articles.setter
    def no_of_articles(self, no_of_articles: int) -> None:
        """Sets the number of articles to find and scrape
        
        Parameters
        ----------
        no_of_articles : int
            The number of articles to find and scrape

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If no_of_articles is not an integer

        Examples
        --------
        >>> from twitternewsbot.twitternewsbot import TwitterNewsBot
        >>> from twitternewsbot.newsfinder import NewsFinder
        >>> from twitternewsbot.tweeter import Tweeter
        >>> bot = TwitterNewsBot(NewsFinder(), Tweeter(), "Python")
        >>> bot.no_of_articles = 10
        """
        # Check if no_of_articles is an integer
        if not isinstance(no_of_articles, int):
            raise TypeError("no_of_articles must be an integer")
        
        self.__no_of_articles = no_of_articles

    def run(self, **kwargs) -> dict:
        """
        Build article list, scrape articles and tweet summarized tweet for the given topic.

        Parameters
        ----------
        **kwargs : dict
            Arguments for Tweeter.tweet function excluding articles_list. See Tweeter.tweet for more details on the args.

        Returns
        -------
        dict
            A dictionary containing the total character count, the number of tweets posted, and the id of the parent tweet when run
        
        Examples
        --------

        Creating a basic pipeline to find, scrape and tweet news articles:

        >>> from twitternewsbot.twitternewsbot import TwitterNewsBot
        >>> from twitternewsbot.newsfinder import NewsFinder
        >>> from twitternewsbot.tweeter import Tweeter
        >>> bot = TwitterNewsBot(NewsFinder(), Tweeter(), "Python")
        >>> bot.run()
        """

        # Run the pipeline
        return self.__build_pipeline(**kwargs)
