# Import statements
from requests_html import HTMLSession
import re
from tweepy import Client
import requests
import google.generativeai as palm

# Global variables
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAK%2F%2BoQEAAAAAOXgBu2%2BUFDIdjR%2FsdM5mTfTOHrQ%3DMB7o7JVafFAjzN6Ljkg8fKmnAA6Ncl2X4Z9dJK8ttbFmQSehlh"
API_KEY = "1hdSiyVqH33XNoLQ7uxfjzFbF"
API_KEY_SECRET = "fuXchiV2xXYL7B7ivomgd2b6va7l6Isya0zVA5PMeW76lhRahE"
ACCESS_TOKEN = "1674314897578946560-moo2kTmeiWoixXO1JoCUv83yP3uDWD"
ACCESS_TOKEN_SECRET = "nzewvmJHGYcYTUgKHD4rG39o2j4DYN4SxBQnPuEu2apNW"
GOOGLE_API_KEY = 'AIzaSyChaW690msMYgvQs3QNV100_pVxpIr5kek'

class Bot():
    """Common API Object"""

    #####################################
    # Initialization
    #####################################

    def __init__(self) -> None:
        """Initialize the Bot class"""
        pass

    #####################################
    # Private Methods
    #####################################

    def __scrape_articles(self, topic: str, number_of_articles: int = 5) -> list | None:
        """Private: Scrape the news articles from Google News for a given topic

        Parameters
        ----------
        topic : str
            The topic to search for
        number_of_articles : int, optional 
            The number of articles to scrape, by default 5

        Returns
        -------
        all_articles : list
            A list of dictionaries containing the title, source, time and link of each article
        """

        # Initialize an HTML Session
        session = HTMLSession()

        # Initalize URL
        query = topic.replace(' ', '+')
        url = f'https://news.google.com/search?for={query}&hl=en-IN&gl=IN&ceid=IN:en'

        # Get the page
        r = session.get(url=url)

        # Get all the articles
        try:
            articles = r.html.find('article')
        except:
            print("No articles found")
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

            # TODO: Block certain sources - www.news18.com and www.dailymail.co.uk

            # Get the time
            time = article.find('time', first=True).text
            numbersRegex = re.compile(r'\d+')
            unitRegex = re.compile(r'hour|day|minute|Yesterday')
            unit = unitRegex.findall(time)
            if unit == []:
                continue
            unit = unit[0]
            if unit != 'Yesterday':
                numbers = numbersRegex.findall(time)[0]
                if (unit != 'hour' and unit != 'minute') and int(numbers) > 1:
                    continue
        
            # Get the link
            link = article.find('a', first=True).absolute_links.pop()

            # Print the details
            newsarticle = {
                'title': title,
                'source': source,
                'time': time,
                'link': link
            }
            all_articles.append(newsarticle)

        return all_articles
    
    def __tweet(self, text: str) -> None:
        """Tweet the given text
        
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

        # TODO: Make use of yield for efficiency
        text = list(self.__create_chunks(text))


        no_of_chunks = len(text)

        # Initialize tweepy Client
        try:
            client = Client(bearer_token=BEARER_TOKEN, 
                            consumer_key=API_KEY,
                            consumer_secret=API_KEY_SECRET,
                            access_token=ACCESS_TOKEN,
                            access_token_secret=ACCESS_TOKEN_SECRET
                            )
        except:
            print("Invalid Twitter API Credentials")

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

    def __scrape_news_article(self, url: str) -> dict | None:
        """Scrape the news article from the given url

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
            print(f"Error processing url: {url}. Continuing without it...")
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
            print("Article cannot be scraped. Continuing without it...")
            return None


        # Join all the paragraphs to form the article
        body = '\n'.join([fragment.text for fragment in article_fragments])

        return {'title': title, 'article': body}


    def __build_article_from_dict(self, article_dict: dict) -> dict | None:
        """Build the article from the given dictionary

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
    
    def __build_list_of_articles(self, articles_list) -> list:
        """Build a list of articles from the given list of dictionaries
        
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
        articles_full_text = []
        for article in articles_list:
            article_text = self.__build_article_from_dict(article)
            if article_text is not None:
                articles_full_text.append(article_text)
        return articles_full_text
    
    def __summarize_article(self, article: dict) -> str | None:
        """Summarize the given article using Google PaLM API

        Parameters
        ----------
        article : dict
            A dictionary containing the title and article body of the news article

        Returns
        -------
        summary : str
            The summary of the article created using GOOGLE PaLM
        """

        # Initialize PaLM
        palm.configure(api_key=GOOGLE_API_KEY)

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
        """

        # Generate the tweet
        try:
            tweet = palm.generate_text(**defaults, prompt=prompt)
            return tweet.result
        except:
            return None
            

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

    def __handle_articles_list(self, articles_list: list, title: str) -> str | None:
        """Handle the list of articles by summarizing them and returning a generated tweet

        Parameters
        ----------
        articles_list : list(dict)
            A list of dictionaries containing the title, source, date and link of the articles
        title : str
            The title of the tweet

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
            summary = self.__summarize_article(article)

            # If summary is None, continue by skipping article
            if summary is None:
                continue

            # Clean the summary
            articles_generated_summary += self.__clean_tweet(summary)

            # Add a new line, formatting
            articles_generated_summary += "\n\n"

        # Return the generated summary
        return articles_generated_summary
    
    ###############################
    # Public Methods - API Methods and CLI Methods
    ###############################