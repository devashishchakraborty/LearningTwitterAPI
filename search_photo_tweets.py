import requests
import re
import concurrent.futures


class TwitterAPI:
    def __init__(self):
        self.url = "https://api.twitter.com/1.1/statuses/user_timeline.json?user_id=3162239370&count=200&trim_user=1"

        self.headers = {'Authorization': r'Bearer AAAAAAAAAAAAAAAAAAAAAAALIAEAAAAAK2H%2FBuXtqJ%2BDBk9pOgDhmVFLN7A%3D5OrUtXJh8YKZjkA3nQDBx7i269M8Uk4Wx2rxO6FzL2HyDyPOmI'}

        self.response = requests.get(self.url, headers=self.headers)
        self.tweet_ids = []
        self.picture_tweet_ids = []

        self.text = self.response.json()
        for ids in self.text:
            self.tweet_ids.append(ids["id_str"])
    
    def thread(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.check_photo_tweets, self.tweet_ids)
        
        print(self.picture_tweet_ids)
    
    def check_photo_tweets(self, id):
        self.url_tweet = f"https://api.twitter.com/2/tweets/{id}?tweet.fields=entities"
        self.tweet_details = requests.get(self.url_tweet, headers=self.headers).json()
        try:
            if self.tweet_details["data"]["entities"]["urls"][0]["expanded_url"].find("/photo") != -1:
                self.picture_tweet_ids.append(id)
            print(self.tweet_details["data"]["entities"]["urls"][0]["expanded_url"])

        except KeyError:
            pass
        

t = TwitterAPI()
t.thread()