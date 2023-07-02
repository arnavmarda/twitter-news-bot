import google.generativeai as palm

def summarize_article(article):

    # Initialize PaLM
    palm.configure(api_key='AIzaSyChaW690msMYgvQs3QNV100_pVxpIr5kek')

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
        
    

def clean_tweet(tweet_text: str):

    # Remove * from tweet
    tweet_text = tweet_text.replace('*', '')
    return tweet_text

def handle_articles_list(articles_list, topic):
    articles_generated_summary = f"{topic}:\n\n"
    for article in articles_list:
        summary = summarize_article(article)
        if summary is None:
            continue
        articles_generated_summary += clean_tweet(summary)
        articles_generated_summary += "\n\n"
    return articles_generated_summary