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
  api.verify_credentials()
  print('API Created')
  return api

def accessapi():
    URL ="https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json"
    r= requests.get(url=URL)
    quote = json.loads(r.content)
    if quote["quoteAuthor"] is None:
      quote["quoteAuthor"] = "Unknown"
    author = "-"+quote["quoteAuthor"]
    tweettopublish=quote["quoteText"]+"\n"+author.rjust(80)
    return tweettopublish

def main():  
  # print(accessapi())
  api=create_api()
  # i=0
  # for status in tweepy.Cursor(api.user_timeline).items(1000):
  #   api.destroy_status(status.id)
  #   print(f"destroyed status{status.id}")
    # i+=1
    # if i<3:
    #   # break
    #   with open('tweets.json','a') as fl:
    #     file2 = open('tw.txt','a')
    #     print(str(status)+"\n\n",file=file2)
    #     fl.write(json.dumps(status._json,indent=1)+"\n")

  while True:
    quote = accessapi()
    api.update_status(quote) 
    print(quote)
    sleep_time = random.randint(2700,3600)
    sleep(sleep_time)

if __name__ == "__main__":
    main()
