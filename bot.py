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

def getquote():
    URL = "https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json"
    raw = requests.get(url=URL)
    quote = json.loads(raw.content)
    if quote["quoteText"].strip()=="":
      sleep(5)
      return getquote()
    if quote["quoteAuthor"].strip()=="":
      quote["quoteAuthor"] = "Unknown"
    author = "By "+quote["quoteAuthor"]
    tweettopublish=quote["quoteText"]+"\n"+author
    return tweettopublish

def main():  
  try:
    api=create_api()
  except Exception as e:
    print(f"Exception encountered in connecting with Twitter.\n{e}")  
  while True:
    quote = getquote()
    api.update_status(quote) 
    print(quote)
    sleep_time = random.randint(1800,3000)
    sleep(sleep_time)
if __name__ == "__main__":
    main()
