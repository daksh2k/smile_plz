import tweepy 
from time import sleep
import requests
import json
from dotenv import load_dotenv
import os
import random

def create_api():
  load_dotenv()  
  consumer_key = os.environ.get("consumer_key")
  consumer_secret = os.environ.get("consumer_secret")
  access_token = os.environ.get("access_token")
  access_token_secret = os.environ.get("access_token_secret")
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
  return api

def accessapi():
    URL ="https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json"
    r= requests.get(url=URL)
    quote = json.loads(r.content)
    if quote["quoteAuthor"] is None:
      quote["quoteAuthor"] = "Unknown"
    author = "By "+quote["quoteAuthor"]
    tweettopublish=quote["quoteText"]+"\n"+author
    return tweettopublish

def main():  
  api=create_api()
  while True:
    quote = accessapi()
    api.update_status(quote) 
    print(quote)
    sleep_time = random.randint(1800,3200)
    sleep(sleep_time)

if __name__ == "__main__":
    main()
