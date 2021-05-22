import tweepy 
from time import sleep
import requests
import json
from dotenv import load_dotenv
import os

def create_api():
  load_dotenv()  
  consumer_key = os.environ.get("consumer_key")
  consumer_secret = os.environ.get("consmer_secret")
  access_token = os.environ.get("access_token")
  access_token_secret = os.environ.get("access_token_secret")
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
  api.verify_credentials()
  print('API Created')
  return api
def accessapi():
    URL ="https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json"
    r= requests.get(url=URL)
    quote=r.text
    tweettopublish=quote
    return tweettopublish

def main():  
  api=create_api()
  while True:
    api.update_status(accessapi()) 
    print(accessapi())
    sleep(120)

if __name__ == "__main__":
    main()
