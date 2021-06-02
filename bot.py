import tweepy 
from time import sleep
import requests
import json
from dotenv import load_dotenv
import os
import random
from pymongo import MongoClient
import keep_alive

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

def insert_tweet(tweet,client):
  db = client.tweetbot
  coll = db.tweets
  twin = {}
  twin["tweetid"] = tweet.id
  twin["tweetText"] = tweet.full_text.replace("By ","-")
  twin["createdDate"] = tweet.created_at
  coll.insert_one(twin)

def check_dup(tweet,client):
  db = client.tweetbot
  coll = db.tweets
  doc_cursor = coll.find({'tweetText': tweet})
  doc_list = list(doc_cursor)
  if len(doc_list) == 0:
    return False
  else:
    return True  

def getquote(client):
    client = MongoClient("mongodb+srv://"+os.environ.get("mongo_us")+":"+os.environ.get("mongo_pw")+"@test.jz2wo.mongodb.net/tweetbot?retryWrites=true&w=majority")
    URL = "https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json"
    raw = requests.get(url=URL)
    if raw.status_code != 200:
      print(f"Cannot get the quote (HTTP {raw.status_code}): {raw.text}\nAPI may be down!")
      sleep(120)
      return getquote(client)
    try:
      quote = json.loads(raw.text.replace("\\",""))
    except Exception as e:
      print(f"Exception:\n{e}\nRetrying again...")
      sleep(5)
      return getquote(client)  
    if quote["quoteText"].strip()=="":
      sleep(5)
      return getquote(client)
    if quote["quoteAuthor"].strip()=="":
      quote["quoteAuthor"] = "Unknown"
    author = "-"+quote["quoteAuthor"]
    tweettopublish=quote["quoteText"]+"\n"+author
    dup = check_dup(tweettopublish,client)
    if dup:
      print(f"Duplicate tweet: {tweettopublish}\nGetting again...")
      sleep(5)
      return getquote(client)
    else:
      return tweettopublish
def main():  
  try:
    api=create_api()
    keep_alive.keep_alive()
    client = MongoClient("mongodb+srv://"+os.environ.get("mongo_us")+":"+os.environ.get("mongo_pw")+"@test.jz2wo.mongodb.net/tweetbot?retryWrites=true&w=majority")
  except Exception as e:
    print(f"Exception encountered in connecting with Twitter.\n{e}")  
  while True:
    tweet = getquote(client)
    twin = api.update_status(tweet,tweet_mode="extended")
    insert_tweet(twin,client)
    print(tweet)
    sleep_time = random.randint(2700,3300)
    sleep(sleep_time)

if __name__ == "__main__":
    main()
