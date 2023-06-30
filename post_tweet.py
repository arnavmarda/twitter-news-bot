from tweepy import Client

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAK%2F%2BoQEAAAAAOXgBu2%2BUFDIdjR%2FsdM5mTfTOHrQ%3DMB7o7JVafFAjzN6Ljkg8fKmnAA6Ncl2X4Z9dJK8ttbFmQSehlh"
API_KEY = "1hdSiyVqH33XNoLQ7uxfjzFbF"
API_KEY_SECRET = "fuXchiV2xXYL7B7ivomgd2b6va7l6Isya0zVA5PMeW76lhRahE"
ACCESS_TOKEN = "1674314897578946560-moo2kTmeiWoixXO1JoCUv83yP3uDWD"
ACCESS_TOKEN_SECRET = "nzewvmJHGYcYTUgKHD4rG39o2j4DYN4SxBQnPuEu2apNW"

def tweet(text):

    # Create chunks
    total_char_count = len(text)
    text = list(create_chunks(text))
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
    parent_tweet_id = parent_tweet(text=parent_tweet_text, client=client)

    # Post children tweets
    for leaf_tweet in leaf_tweets:
        child_tweet(text=leaf_tweet, client=client, parent_tweet_id=parent_tweet_id)

    print(f"{total_char_count} char tweet posted succesfully in {no_of_chunks} chunks.")


    

def parent_tweet(text: str, client: Client) -> str:
    try:
        parent_tweet_id = client.create_tweet(text=text).data['id']
        return parent_tweet_id
    except Exception as error:
        print(f"Tweet not posted succesfully: {error}")

def child_tweet(text: str, client: Client, parent_tweet_id: str):
    try:
        client.create_tweet(text=text, in_reply_to_tweet_id=parent_tweet_id)
    except Exception as error:
        print(f"Tweet not posted succesfully: {error}")


def create_chunks(text):
    for start in range(0, len(text), 280):
        yield text[start:start + 280]
