import tweepy as xpy
from textblob import TextBlob
import re


class XClient:

    def __init__(self):
        api_key = 'PASTE_HERE'
        api_key_secret = 'PASTE_HERE'
        access_token = 'PASTE_HERE'
        access_token_secret = 'PASTE_HERE'

        try:
            self.auth = xpy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)

            self.api = xpy.API(self.auth)
        except:
            print('Error: Authentication failed!')
        
        # self.client.search_recent_tweets('Programming', tweet_fields=['context_annotations', 'created_at'], max_results=10)
    
    def clean_post(self, post):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", post).split())

    def get_sentiment(self, post):
        analysis = TextBlob(self.clean_post(post))
        sentiment = analysis.sentiment.polarity

        if sentiment > 0:
            return 'positive'
        elif sentiment < 0:
            return 'negative'
        else:
            return 'neutral'
    
    def get_posts(self, query, count=10):
        
        posts = []

        try:
            fetched_posts = self.api.search_tweets(query, count=count)
        except xpy.TweepyException as e:
            print(f'Error while getting posts: {e}')
            exit(1)
        
        for post in fetched_posts:
            parsed_post = {}

            parsed_post['text'] = post.text
            parsed_post['sentiment'] = self.get_sentiment(post.text)

            if post.retweet_count > 0:
                if parsed_post not in posts:
                    posts.append(parsed_post)
            else:
                posts.append(parsed_post)
        
        return posts


def main():
    api = XClient()

    posts = api.get_posts(query='Programming', count=10)

    pos_posts = [post for post in posts if post['sentiment'] == 'positive']
    print('Percentage of positive posts: {:.2f}%'.format(len(pos_posts) / len(posts) * 100))

    neg_posts = [post for post in posts if post['sentiment'] == 'negative']
    print('Percentage of negative posts: {:.2f}%'.format(len(neg_posts) / len(posts) * 100))

    print('Positive posts: ')
    for post in pos_posts:
        print(f'--> {post["text"]}')
    
    print('Negative posts: ')
    for post in neg_posts:
        print(f'--> {post["text"]}')
    


if __name__ == '__main__':
    main()
