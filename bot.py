import tweepy 
from time import sleep
import requests
import json
import os
import sys
import random

from dotenv import load_dotenv
from pymongo import MongoClient

import retquote as rq
import tweetq as tq

# Connect with Twitter Account
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

#Insert tweet in Database
def insert_tweet(tweet,client):
  db = client.tweetbot
  coll = db.tweets
  twin = {
    "tweetid": tweet.id,
    "tweetText": tweet.full_text,
    "createdDate": tweet.created_at}
  coll.insert_one(twin)

#Get Quote and parse it
def getquote(client):
    client = client
    URL = "https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json"
    raw = requests.get(url=URL)
    if raw.status_code != 200:
      print(f"Cannot get the quote (HTTP {raw.status_code}): {raw.text}\nAPI may be down!")
      sleep(120)
      return getquote(client)
    try:
      quote = json.loads(raw.text.replace("\\",""))
    except Exception as e:
      print(f"{raw.text}\nException:\n{e}\nRetrying again...")
      sleep(5)
      return getquote(client)  
    if quote["quoteText"].strip()=="":
      sleep(5)
      return getquote(client)
    if quote["quoteAuthor"].strip()=="":
      quote["quoteAuthor"] = "Unknown"
    author = "-"+quote["quoteAuthor"].strip()
    # author= textmanup(author,typem="bold")
    tweettopublish=quote["quoteText"].strip()+"\n"+author
    return tweettopublish
  
# Follow back every user
def follow_followers(api):
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            print(f"Following {follower.name}")
            follower.follow()

# Make the text bold, italic or bolditalic      
def textmanup(input_text,typem="bold"):
    chars = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789"
    bold_chars = "𝗤𝗪𝗘𝗥𝗧𝗬𝗨𝗜𝗢𝗣𝗔𝗦𝗗𝗙𝗚𝗛𝗝𝗞𝗟𝗭𝗫𝗖𝗩𝗕𝗡𝗠𝗾𝘄𝗲𝗿𝘁𝘆𝘂𝗶𝗼𝗽𝗮𝘀𝗱𝗳𝗴𝗵𝗷𝗸𝗹𝘇𝘅𝗰𝘃𝗯𝗻𝗺𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"
    itlaics_chars  ="𝘘𝘞𝘌𝘙𝘛𝘠𝘜𝘐𝘖𝘗𝘈𝘚𝘋𝘍𝘎𝘏𝘑𝘒𝘓𝘡𝘟𝘊𝘝𝘉𝘕𝘔𝘲𝘸𝘦𝘳𝘵𝘺𝘶𝘪𝘰𝘱𝘢𝘴𝘥𝘧𝘨𝘩𝘫𝘬𝘭𝘻𝘹𝘤𝘷𝘣𝘯𝘮0123456789"
    bold_italics_chars = "𝙌𝙒𝙀𝙍𝙏𝙔𝙐𝙄𝙊𝙋𝘼𝙎𝘿𝙁𝙂𝙃𝙅𝙆𝙇𝙕𝙓𝘾𝙑𝘽𝙉𝙈𝙦𝙬𝙚𝙧𝙩𝙮𝙪𝙞𝙤𝙥𝙖𝙨𝙙𝙛𝙜𝙝𝙟𝙠𝙡𝙯𝙭𝙘𝙫𝙗𝙣𝙢0123456789"
    output = ""
    for character in input_text:
        if character in chars:
          if typem=="bold":
            output += bold_chars[chars.index(character)]
          elif typem=="italic":
            output += itlaics_chars[chars.index(character)]  
          elif typem=="bolditalic":
            output += bold_italics_chars[chars.index(character)] 
        else:
            output += character 
    return output

def main():  
  try:
    api=create_api()
    client = MongoClient(os.environ.get("database_uri"))
  except Exception as e:
    print(f"Exception encountered in connecting with Database or Twitter.Check the credentials again!\n{e}") 
    sys.exit()
  while True:
    try:
      follow_followers(api)
    except:
      pass
    try:
      quote = rq.main(client)
      tweet,t2 = tq.tweet_quote(api,quote)
    except Exception as e:
      print(f"Problem getting Quote! DB may be down. Using API for Quote.\n{e}")
      quote = getquote(client)
      tweet,t2 = tq.tweet_dbdown(api,quote)
    try: 
      insert_tweet(tweet,client)
      print(tweet.full_text)
      if t2 is not None:
        insert_tweet(t2,client)
        print(t2.full_text)
    except Exception as e:
      print(f"Error inserting in tweet collections!\n{e}")  
    sleep_time = random.randint(60*52, 60*58)
    sleep(sleep_time)

if __name__ == "__main__":
    main()