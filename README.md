# Smile Please
 A simple Twitter bot tweeting quotes hourly.
 Deployed on **[Replit](https://www.replit.com/@smileplz/smile-plz)**.
 
 Also with a duplicate tweet check using tweets stored in MongoDB hosted at [Mongo Atlas](https://www.mongodb.com/cloud).
 
 Checkout the tweets at:
 - ### Check out the bot at this [twitter profile.](https://twitter.com/smile_plz12)
 ![alt text](./images/timeline_p.png "Website image")
 - ### Or on the  [Replit Website](https://smile-plz.smileplz.repl.co/) where timeline is shown using twitter widgets.

![alt text](./images/timeline_w.png "Website image")
## Usage
 For using this bot clone this repositary and install the dependencies from the [requirements](./requirements.txt) file.
 
- Enter your details in a .env file like this:

  - consumer_key = "XXXXXXXXXXXXXXXXXXXX"
  - consumer_secret = "XXXXXXXXXXXXXXXXXXXXXX" 
  - access_token = "XXXXXXXXXXXXXXXXXXXXXXX" 
  - access_token_secret = "XXXXXXXXXXXXXXXXXXXX" 
  - mongo_pw = "Your mongo atlas password"
  - mongo_us = "Your mongo atlas username"
- Or set these variables in your deployed environment.

Then run the [bot.py](./bot.py) file to execute your bot.
## Get these variables from your Twitter Developer Account [here](https://developer.twitter.com/en/portal/projects-and-apps).