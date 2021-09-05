import tweepy
import os
from time import sleep

# Connect with Twitter Account
def create_api():
  """
  Get the required secrets from environment.
  If platform_type is local load the .env file for loading secrets
  If authentication fails or any exception print the exception and retry after 5 minutes
  """
  try:
    if os.environ.get("platform_type","local")=="local":
      from dotenv import load_dotenv
      load_dotenv()  
    consumer_key = os.environ.get("consumer_key")
    consumer_secret = os.environ.get("consumer_secret")
    access_token = os.environ.get("access_token")
    access_token_secret = os.environ.get("access_token_secret")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True,  wait_on_rate_limit_notify=True)
    return api
  except Exception as e:
    print(e)
    sleep(300)
    return create_api()
