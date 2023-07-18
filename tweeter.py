import google.generativeai as palm
from tweepy import Client
import os

class Tweeter():

  #####################################
  # Initialization
  #####################################
    
    def __init__(self):
        """Initialize the class with tokens and tweepy client"""
        try:
            self.__BEARER_TOKEN = os.environ['BEARER_TOKEN']
        except:
            raise Exception("BEARER_TOKEN not found in environment variables")

        try:
            self.__client = Client(bearer_token=self.__BEARER_TOKEN)
        except:
            raise Exception("Authentication Failed. Invalid Twitter API Credentials")
    


  #####################################
  # Private Methods
  #####################################

    def __tweet(self, text: str) -> None:
        """Private: Tweet the given text
        
        Parameters
        ----------
        text : str
            The text to be tweeted

        Returns
        -------
        None
        """

        # Create chunks
        total_char_count = len(text)
        text = list(self.__create_chunks(text))


        no_of_chunks = len(text)

        client = self.__client

        # Seperate parent tweet from children tweets
        parent_tweet_text = text[0]
        leaf_tweets = text[1:]

        # Post parent tweet
        parent_tweet_id = self.__parent_tweet(text=parent_tweet_text, client=client)

        # Post children tweets
        for leaf_tweet in leaf_tweets:
            self.__child_tweet(text=leaf_tweet, client=client, parent_tweet_id=parent_tweet_id)

        print(f"{total_char_count} char tweet posted succesfully in {no_of_chunks} chunks.")

    def __parent_tweet(text: str, client: Client) -> str | None:
        """Post the parent tweet and return the id of the tweet
        
        Parameters
        ----------
        text : str
            The text to be tweeted
        client : Client
            The tweepy client object i.e. user to post the tweet
        
        Returns
        -------
        parent_tweet_id : str
            The id of the tweet
        """
        try:
            parent_tweet_id = client.create_tweet(text=text).data['id']
            return parent_tweet_id
        except Exception as error:
            print(f"Tweet not posted succesfully: {error}")

    def __child_tweet(text: str, client: Client, parent_tweet_id: str) -> None:
        """Post the child tweet as a reply to the parent tweet
        
        Parameters
        ----------
        text : str
            The text to be tweeted as a reply to the parent tweet
        client : Client
            The tweepy client object i.e. user to post the tweet
        parent_tweet_id : str
            The id of the parent tweet

        Returns
        -------
        None
        """
        try:
            client.create_tweet(text=text, in_reply_to_tweet_id=parent_tweet_id)
        except Exception as error:
            print(f"Tweet not posted succesfully: {error}")


    def __create_chunks(text: str) -> list(str):
        """Create chunks of 280 characters each from the given text while leveraging the yield keyword
        
        Parameters
        ----------
        text : str
            The text to be chunked

        Returns
        -------
        chunks : list(str)
            A list of 280 char chunks of the given text
        """
        for start in range(0, len(text), 280):
            yield text[start:start + 280]

    
    def __summarize_article(self, article: dict, prompt: str|None) -> str | None:
        """Summarize the given article using Google PaLM API

        Parameters
        ----------
        article : dict
            A dictionary containing the title and article body of the news article
        prompt : str, optional
            The prompt to be used for the summarization, by default None

        Returns
        -------
        summary : str
            The summary of the article created using GOOGLE PaLM
        """

        # Get the API key
        try:
            GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
        except:
            raise Exception("GOOGLE_API_KEY not found in environment variables")

        # Initialize PaLM
        try:
            palm.configure(api_key=GOOGLE_API_KEY)
        except:
            raise Exception("Authentication Failed. Invalid Google API Credentials")

        # Default Settings
        defaults = {
                        'model': 'models/text-bison-001',
                        'temperature': 0.1,
                        'candidate_count': 1,
                        'top_k': 40,
                        'top_p': 0.95,
                        'max_output_tokens': 1024,
                        'stop_sequences': [],
                        'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":1},{"category":"HARM_CATEGORY_TOXICITY","threshold":1},{"category":"HARM_CATEGORY_VIOLENCE","threshold":2},{"category":"HARM_CATEGORY_SEXUAL","threshold":2},{"category":"HARM_CATEGORY_MEDICAL","threshold":2},{"category":"HARM_CATEGORY_DANGEROUS","threshold":2}],
                    }
        
        # Create a prompt
        prompt = f"""
        Summarize the following article and condense it into 2 bullet points. Add the title of the article at the top. Do not leave an empty line after the article. Only use information from the article provided below. Structure your response as follows:

        Format for Summary:
        Title
        - Bullet point 1
        - Bullet point 2

        Title - {article['title']}
        Article - {article['article']}

        Summary:
        """ if prompt is None else f"""{prompt}"""

        # Generate the tweet
        try:
            tweet = palm.generate_text(**defaults, prompt=prompt)
            return tweet.result
        except:
            raise Exception("Failed to generate tweet using PaLM")
            

    def __clean_tweet(self, tweet_text: str) -> str:
        """Clean the tweet by removing unwanted characters as PaLM adds '*' to the tweet occasionally

        Parameters
        ----------
        tweet_text : str
            The text of the tweet to be cleaned

        Returns
        -------
        tweet_text : str
            The cleaned tweet text
        """

        # Remove * from tweet
        tweet_text = tweet_text.replace('*', '')
        return tweet_text

    def __handle_articles_list(self, articles_list: list, title: str|None, prompt: str|None) -> str | None:
        """Handle the list of articles by summarizing them and returning a generated tweet

        Parameters
        ----------
        articles_list : list(dict)
            A list of dictionaries containing the title, source, date and link of the articles
        title : str, optional
            The title of the tweet
        prompt : str, optional
            The prompt to be used for the summarization, by default None

        Returns
        -------
        articles_generated_summary : str
            The generated tweet from the articles
        """

        # Add title of tweet to the beginning of the tweet
        articles_generated_summary = f"{title}:\n\n"

        # Add the summary for each article to the tweet
        for article in articles_list:
            # Call API to get summary
            summary = self.__summarize_article(article, prompt)

            # If summary is None, continue by skipping article
            if summary is None:
                continue

            # Clean the summary
            articles_generated_summary += self.__clean_tweet(summary)

            # Add a new line, formatting
            articles_generated_summary += "\n\n"

        # Return the generated summary
        return articles_generated_summary
    
    def __generate_with_palm(self, prompt: str|None) -> str | None:
        """Generate a tweet using PaLM

        Parameters
        ----------
        prompt : str, optional
            The prompt to be used for generation, by default None
        to_rewrite : str, optional
            The text to be rewritten, by default None
        Returns
        -------
        generated_summary : str
            The generated tweet
        """

        # Get the API key
        try:
            GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
        except:
            raise Exception("GOOGLE_API_KEY not found in environment variables")

        # Initialize PaLM
        try:
            palm.configure(api_key=GOOGLE_API_KEY)
        except:
            raise Exception("Authentication Failed. Invalid Google API Credentials")
        
        # Default Settings
        defaults = {
                        'model': 'models/text-bison-001',
                        'temperature': 0.1,
                        'candidate_count': 1,
                        'top_k': 40,
                        'top_p': 0.95,
                        'max_output_tokens': 1024,
                        'stop_sequences': [],
                        'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":1},{"category":"HARM_CATEGORY_TOXICITY","threshold":1},{"category":"HARM_CATEGORY_VIOLENCE","threshold":2},{"category":"HARM_CATEGORY_SEXUAL","threshold":2},{"category":"HARM_CATEGORY_MEDICAL","threshold":2},{"category":"HARM_CATEGORY_DANGEROUS","threshold":2}],
                    }
        
        # Generate the tweet
        try:
            tweet = palm.generate_text(**defaults, prompt=prompt)
            return tweet.result
        except:
            raise Exception("Failed to generate tweet using PaLM")
        

        

  #####################################
  # Public Methods - API Methods
  #####################################

    def get_client(self) -> Client:
        """Get the tweepy client object

        Returns
        -------
        client : Client
            The tweepy client object
        """
        return self.__client

    def tweet(self, title: str|None, tweet: str|None, articles_list: list|None, use_palm: bool|None, prompt: str|None) -> None:
        """Tweet the given articles list

        Parameters
        ----------
        title : str, optional
            The title of the tweet
        tweet : str, optional
            The tweet to be posted
        articles_list : list, optional
            A list of dictionaries containing the title, source, link and text of the articles.
            Obtained from the NewsFinder.get_news_articles() method
        use_palm : bool, optional
            A boolean value indicating whether to use PaLM to generate tweet with prompt
        prompt : str, optional
            The prompt to be used for the summarization with PaLM
        rewrite_with_AI : bool, optional
            A boolean value indicating whether to rewrite the tweet with AI or not according to prompt

        Returns
        -------
        None
        """

        # Check if title is valid
        if title is not None and not isinstance(title, str):
            raise TypeError("title must be a string")
        
        # Check if tweet is valid
        if tweet is not None and not isinstance(tweet, str):
            raise TypeError("tweet must be a string")
        
        # Check if articles_list is valid
        if articles_list is not None and not isinstance(articles_list, list(dict)):
            raise TypeError("articles_list must be a list of dicts")
        
        # Check if use_palm is valid
        if use_palm is not None and not isinstance(use_palm, bool):
            raise TypeError("use_palm must be a boolean")
        
        # Check if use_palm is True, then tweet and articles_list must be None
        if use_palm is True and (tweet is not None or articles_list is not None):
            raise ValueError("tweet and articles_list must be None if use_palm is True")
        
        # Check if prompt is not provided and use_palm is True
        if prompt is None and use_palm is True:
            raise ValueError("prompt must be provided if use_palm is True")

        # Check if tweet and articles_list are both provided
        if tweet is not None and articles_list is not None:
            raise ValueError("Both tweet and articles_list cannot be provided")
        
        # Check if prompt is valid
        if prompt is not None and not isinstance(prompt, str):
            raise TypeError("prompt must be a string")
        
        if articles_list is not None:
            # Handle the articles list
            tweet = self.__handle_articles_list(articles_list, title, prompt)
        elif use_palm:
            # Generate a tweet using PaLM
            tweet = self.__generate_with_palm(prompt)
            if title is not None:
                tweet = f"{title}:\n\n{tweet}"
        
        self.__tweet(tweet)
        

        
        
        