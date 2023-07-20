# Import statements
from newsfinder import NewsFinder
from tweeter import Tweeter
import os

class TwitterNewsBot():
    """
    API Object to connect the NewsFinder and Tweeter classes to build a pipeline to automate finding, scraping and tweeting news.
    Build a .yaml file if needed for Github Actions to run the cron job.
    """

    #####################################
    # Initialization
    #####################################

    def __init__(self, news_finder: NewsFinder, tweeter_obj: Tweeter, topic: str, no_of_articles: int|None = 5):
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
        self.topic = topic
        self.no_of_articles = no_of_articles

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
        articles = self.news_finder.get_news_articles(topic=self.topic, number_of_articles=self.no_of_articles)
        return self.tweeter_obj.tweet(articles_list=articles, **kwargs)
    
    def __give_yaml_text(self, cron: str, file: str) -> str:
        """Private: Build the .yaml file text for Github Actions to run the cron job
        
        Parameters
        ----------
        cron : str
            The cron job to run the pipeline.
            You can get a formatted cron job string from https://crontab.guru/
        file : str
            The file to run the pipeline from

        Returns
        -------
        str
            The .yaml file text for Github Actions to run the cron job
        """
        
        # Build the .yaml file text
        text = yaml_file = f"""---
name: "Twitter News Bot"
on:
  schedule:
    - cron: '{cron}'

jobs:
  python-job:
    name: "Python job"
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
      - name: Setup python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11.3'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run python script
        run: python {file}"""

        return text

    
    
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
        """
        return self.topic

    @topic.setter
    def topic(self, topic: str) -> None:
        """Sets the topic to search for news articles
        
        Parameters
        ----------
        topic : str
            The topic to search for news articles

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If topic is not a string
        """
        # Check if topic is a string
        if not isinstance(topic, str):
            raise TypeError("topic must be a string")
        
        self.topic = topic

    @property
    def no_of_articles(self) -> int:
        """Returns the number of articles to find and scrape
        
        Returns
        -------
        int
            The number of articles to find and scrape
        """
        return self.no_of_articles
    
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
        """
        # Check if no_of_articles is an integer
        if not isinstance(no_of_articles, int):
            raise TypeError("no_of_articles must be an integer")
        
        self.no_of_articles = no_of_articles

    def run_pipeline(self, **kwargs) -> dict:
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
        """

        # Run the pipeline
        return self.__build_pipeline(**kwargs)
    
    def build_yaml(self, cron: str, file: str) -> None:
        """Build a .yaml file for Github Actions to run the cron job
        
        Parameters
        ----------
        cron : str
            The cron job to run the pipeline.
            You can get a formatted cron job string from https://crontab.guru/
        file : str
            The file to run the pipeline from

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If cron is not a string
            If file is not a string
        """

        # Check if cron is a string
        if not isinstance(cron, str):
            raise TypeError("cron must be a string")
        
        # Check if file is a string
        if not isinstance(file, str):
            raise TypeError("file must be a string")
        
        # Build the .yml file
        text = self.__give_yaml_text(cron=cron, file=file)

        try:
            os.mkdir(".github")
        except FileExistsError:
            pass

        try:
            os.mkdir(".github/workflows")
        except FileExistsError:
            pass

        file = open(".github/workflows/python-app.yml", "w")
        file.write(text)
        file.close()
        

    