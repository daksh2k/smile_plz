import tweepy 
import requests
import json
import os
import sys
import random
import datetime
from time import sleep

# Import relevant files
import twitter
import retquote as rq
import tweetq as tq

#Insert tweet in database
def insert_tweet(tweet,client):
  """
  Inserting tweets in a different collection just for logging purposes
  can be skipped if wanted.
  """
  db = client.tweetbot
  coll = db.tweets
  twin = {
    "tweetid": tweet.id,
    "tweetText": tweet.full_text,
    "createdDate": tweet.created_at}
  coll.insert_one(twin)
  print(f"{rq.current_time()}Successfully inserted in secondary collection!") 

#Get quote from API and parse and format it
def getquote():
    URL = "https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json"
    raw = requests.get(url=URL)
    if raw.status_code != 200:
      print(f"{rq.current_time()}Cannot get the quote (HTTP {raw.status_code}): {raw.text}\nAPI may be down!")
      sleep(120)
      return getquote()
    try:
      quote = json.loads(raw.text.replace("\\",""))
    except Exception as e:
      print(f"{rq.current_time()}\n{raw.text}\nException:\n{e}\nRetrying again...")
      sleep(5)
      return getquote()  
    if quote["quoteText"].strip()=="":
      sleep(5)
      return getquote()
    if quote["quoteAuthor"].strip()=="":
      quote["quoteAuthor"] = "Unknown"
    author = "–"+quote["quoteAuthor"].strip()
    # author= textmanup(author,typem="bold")
    tweettopublish=quote["quoteText"].strip()+"\n"+author
    print(f"{rq.current_time()}Returned quote from API-:\n{tweettopublish}")
    return tweettopublish
  
# Follow back every user
def follow_followers(api):
    """
    Check the followers list and see if the user is being
    followed by the bot if not follow the user.
    """
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            print(f"{rq.current_time()}Following {follower.name}")
            follower.follow()

# Make the text bold, italic or bolditalic      
def textmanup(input_text,typem="bold"):
    """
    Twitter does not support formatting the text so to format the text
    we can use certain unicode chars and replace the letters with these unicode chars
    for getting the desired result but these unicode chars may increase the length of the text.
    """
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
  """
  Connect with the twitter API.
  Connect with the Mongo Atlas Instance when using db for getting quotes.
  
  Load the log files from the replit db when logging is on and platform is replit.
  Replit db only stores the log files as they cannot be stored directly
  in the filesystem as it is not persistent. 
  
  Execute keep_alive for showing twitter profile and displaying logs
  The keep_alive function along with Uptime Robot helps keep the replit running.
  See https://bit.ly/3h5ZS09 for more detials!

  If logging is on then redirect the default stdout to a log file,
  according to the day and delete any log files older than 14 days.

  After tweeting insert the tweets in a secondary collection
  in the db and print/log those tweets.
  Reset the stdout to default if previously changed.
  Update the current day's log/key in replit db and sleep.
  """
  try:
    api= twitter.create_api()
    if os.environ.get("quote_method","db"=="db"):
      from pymongo import MongoClient
      client = MongoClient(os.environ.get("database_uri"))
    if os.environ.get("platform_type","local")=="replit":
      from keep_alive import keep_alive
      keep_alive()
      if os.environ.get("logging","off")=="on":
        import saveindb as sdb
        sdb.load_files()
  except Exception as e:
    print(f"{rq.current_time()}Exception encountered in connecting with Database or Twitter.Check the credentials again!\n{rq.current_time()}{e}") 
    sys.exit()
  
  # Keep tweeting every hour until forever
  while True:
    del_old = False 
    if os.environ.get("logging","off")=="on":
      log_date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5,minutes=30))) # Get date for IST
      old_log  = f"Logs/log_{(log_date-datetime.timedelta(days=15)).strftime('%d_%m_%y')}.txt"
      curr_log = f"Logs/log_{log_date.strftime('%d_%m_%y')}.txt"
      sys.stdout = open(curr_log,"a",encoding="utf-8")
      if os.path.isfile(old_log):
        os.remove(old_log)
        if os.environ.get("platform_type","local")=="replit":
          sdb.clean_db(old_log)
        del_old = True
    print(f"\n{rq.current_time()}New tweet session!")
    if del_old:
      print(f"{rq.current_time()}Removed old log! {old_log}")
    try:
      follow_followers(api)
    except tweepy.TweepError:
      pass
    try:
      if os.environ.get("quote_method","db")=="db":
        quote = rq.main(client)
        tweet,t2 = tq.tweet_quote(api,quote)
      else:
        quote = getquote()
        tweet,t2 = tq.tweet_dbdown(api,quote)
    except Exception as e:
      print(f"{rq.current_time()}Problem getting Quote! DB may be down. Using API for Quote.\n{rq.current_time()}{e}")
      quote = getquote()
      tweet,t2 = tq.tweet_dbdown(api,quote)
    try:
      if os.environ.get("quote_method","db")=="db":
        insert_tweet(tweet,client)
      print(f"{rq.current_time()}Tweet Sent-:\nTweetId: {tweet.id}\n{tweet.full_text}")
      if t2 is not None:
        if os.environ.get("quote_method","db")=="db":
          insert_tweet(t2,client)
        print(f"{rq.current_time()}2nd Tweet Sent-:\nTweetId: {t2.id}\n{t2.full_text}")
    except Exception as e:
      print(f"{rq.current_time()}Error inserting in tweet collections!\n{rq.current_time()}{e}")  
    sleep_time = random.randint(60*52, 60*58)
    if os.environ.get("logging","off")=="on":
       sys.stdout.flush()
       os.close(sys.stdout.fileno())
       sys.stdout = sys.__stdout__
       if os.environ.get("platform_type","local")=="replit":
         sdb.save_file(curr_log)
    sleep(sleep_time)

if __name__ == "__main__":
    main()