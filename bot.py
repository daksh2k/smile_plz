import tweepy 
from time import sleep
import requests
import json
from dotenv import load_dotenv
import os
import random
from pymongo import MongoClient

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
def insert_tweet(tweet,client,ind):
  db = client.tweetbot
  coll = db.tweets
  tagsrepl =["\n#quotes #wisdom #nature #life #motivation #inspiration",
  "\n#quotes #nature #life #wisdom #motivation",
  "\n#quotes #wisdom #nature #life #inspiration",
  "\n#quotes #wisdom #nature #motivation #inspiration",
  "\n#quotes #wisdom #life #motivation #inspiration",
  "\n#quotes #nature #life #motivation #inspiration"]
  twin = {}
  twin["tweetid"] = tweet.id
  twin["tweetText"] = tweet.full_text.replace(tagsrepl[ind],"")
  twin["createdDate"] = tweet.created_at
  coll.insert_one(twin)

#Check for a Duplicate Tweet
def check_dup(tweet,client):
  db = client.tweetbot
  coll = db.tweets
  doc_cursor = coll.find({'tweetText': tweet})
  doc_list = list(doc_cursor)
  if len(doc_list) == 0:
    return False
  else:
    return True  

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
    author = "-"+quote["quoteAuthor"]
    # author= textmanup(author,typem="bold")
    tweettopublish=quote["quoteText"]+"\n"+author
    dup = check_dup(tweettopublish,client)
    if dup:
      print(f"Duplicate tweet: {tweettopublish}\nGetting again...")
      sleep(5)
      return getquote(client)
    else:
      return tweettopublish

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
    print(f"Exception encountered in connecting with Twitter.\n{e}")  
  while True:
    tweet = getquote(client)
    tags = ["\n#quotes #wisdom #nature #life #motivation #inspiration",
    "\n#quotes #nature #life #wisdom #motivation",
    "\n#quotes #wisdom #nature #life #inspiration",
    "\n#quotes #wisdom #nature #motivation #inspiration",
    "\n#quotes #wisdom #life #motivation #inspiration",
    "\n#quotes #nature #life #motivation #inspiration"]
    ind = random.randint(0,5)
    twin = api.update_status(tweet+tags[ind],tweet_mode="extended")
    insert_tweet(twin,client,ind)
    print(twin.full_text)
    sleep_time = random.randint(2400,3000)
    sleep(sleep_time)

if __name__ == "__main__":
    main()
