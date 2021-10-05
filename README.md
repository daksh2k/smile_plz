# Smile Please
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/daksh2k/smile_plz/blob/master/LICENSE)
[![CodeFactor](https://www.codefactor.io/repository/github/daksh2k/smile_plz/badge/master)](https://www.codefactor.io/repository/github/daksh2k/smile_plz/overview/master)
[![GitHub last commit](https://img.shields.io/github/last-commit/daksh2k/smile_plz)](https://github.com/daksh2k/smile_plz)
[![GitHub issues](https://img.shields.io/github/issues/daksh2k/smile_plz)](https://github.com/daksh2k/smile_plz/issues)
[![Total Lines Of Code](https://tokei.rs/b1/github/daksh2k/smile_plz)](https://github.com/daksh2k/smile_plz)
[![GitHub repo size](https://img.shields.io/github/repo-size/daksh2k/smile_plz)](https://github.com/daksh2k/smile_plz)
[![GitHub top language](https://img.shields.io/github/languages/top/daksh2k/smile_plz)](https://github.com/daksh2k/smile_plz) 

 Twitter bot which tweets a new random quote hourly.
 Deployed on **[Replit](https://www.replit.com/@smileplz/smile-plz)**.

 Quotes are from a custom 500k quotes dataset made from **[Goodreads](https://www.goodreads.com/quotes)** stored in MongoDB hosted at **[Mongo Atlas](https://www.mongodb.com/cloud/atlas)**.
 
 There is also a secondary method for getting quotes using the **[Forismatic API](https://forismatic.com/en/api/)**, which is added as a fallback which can be used as a default.
 
 The bot also has support for dividing the tweet in 2 if it is longer than 280 chars.
 
 Checkout the tweets at:
 - ### Check out the bot at this **[Twitter Profile.](https://twitter.com/smile_plz12)**
  <img src="https://raw.githubusercontent.com/daksh2k/smile_plz/master/images/timeline_p.png" alt="Profile Image" width="550" height="auto"/>

 - ### Or on the **[Replit Website](https://smile-plz.smileplz.repl.co/)** where timeline is shown using **[Twitter Widgets](https://developer.twitter.com/en/docs/twitter-for-websites/timelines/overview)**.
  <img src="https://raw.githubusercontent.com/daksh2k/smile_plz/master/images/timeline_w.png" alt="Profile Image" width="650" height="auto"/>

## Prerequisites
- Get the twitter credentials from your Twitter Developer Account [here](https://developer.twitter.com/en/portal/projects-and-apps).
- By default the bot uses the db for quotes. If you want to use the API by default set `quote-method` environment variable to `api`.
- To get access to Mongo Atlas. Register on [MongoDB Cloud](https://www.mongodb.com/cloud/atlas/register).
- For hosting. Register on [Replit](https://replit.com/signup) or choose any other provider of your choice.
## Usage
 For using this bot clone this repositary and install the dependencies from the [requirements](./requirements.txt) file.
 
- Enter your details in a .env file like this(for **Local Environment** ):
  - consumer_key        = "XXXXXXXXXXXXXXXXXXXX"
  - consumer_secret     = "XXXXXXXXXXXXXXXXXXXXXX" 
  - access_token        = "XXXXXXXXXXXXXXXXXXXXXXX" 
  - access_token_secret = "XXXXXXXXXXXXXXXXXXXX" 
  
- Optional variables-:
  - quote_method    = "db or api" (`db` by default)
  - database_uri    = "Your Mongo Atlas URI" (Required if `quote_method` is db)
  - platform_type   = "local,replit"  (`local` by default )
  - twitter_profile = "twitter profile url" (`https://twitter.com/smile_plz12` by default)
  - logging         = "off or on" (`off` by default)
  - HOST            = "Host url" (`localhost` by default)
  - PORT            = "Port number"(`8080` ny default)

- ### Or set these variables in your deployed environment.

### Then run the [main.py](./main.py) file to execute your bot.
