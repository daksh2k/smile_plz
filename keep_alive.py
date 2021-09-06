from flask import Flask,render_template,abort,send_file,request
from flask_compress import Compress
from threading import Thread
import datetime
import os
import re
import twitter

app = Flask(__name__)
Compress(app)

# Parse the Log File to get Individual Tweet Sessions
def calculate_sessions(log_file_lines):
  final_list = []
  session_list= []
  for line in log_file_lines:
    if not line.strip():
        if session_list:
            final_list.append(session_list)
        session_list=[]
    else:
       session_list.append(line)    
  final_list.append(session_list)
  final_list = [[str(i+1)+". "+l for i,l in enumerate(session)] for session in final_list]
  final_list.reverse()
  return final_list

# Return the List of all Log Files Present in the System
def get_all():
  log_list = [re.search(r"log_(\d{2}_\d{2}_\d{2})",log_file).group(1).replace("_","/") for log_file in os.listdir('Logs')]
  log_list.sort(key = lambda date: datetime.datetime.strptime(date, '%d/%m/%y'),reverse=True)
  log_dict = {}
  for logf in log_list:
     log_file = open(f"Logs/log_{logf.replace('/','_')}.txt","r",encoding="utf-8")
     log_file_lines = log_file.readlines()
     log_file.close()
     log_dict[logf] = f"{len(calculate_sessions(log_file_lines))}"
  return log_dict 

# Get the Summary for current day and overall Profile 
def calculate_summary(fin_list):
  api = twitter.create_api()
  getstats = api.me()
  tweets_to_get = []
  for session in fin_list:
    for line in session:
        if line.strip().find('TweetId')!=-1:
            tweets_to_get.append(line.split(' ')[2].strip())
  tot_favs  = 0
  tot_rts   = 0
  tweets = api.statuses_lookup(tweets_to_get,trim_user=True)
  for tweet in tweets:
    tot_favs  += tweet.favorite_count
    tot_rts   += tweet.retweet_count  
  summary = {
     "Tweets Sent Today" : len(fin_list),
     "Favourites Today"  : tot_favs,
     "Retweets Today"    : tot_rts,
     "Total Tweets Sent" : getstats.statuses_count,
     "Total Followers"   : getstats.followers_count,
     "Total Following"   : getstats.friends_count
  }
  return summary

# Base Route for showing twitter profile
@app.route('/',methods=['GET'])
def main():
  return render_template("index.html",profile=os.environ.get("twitter_profile","https://twitter.com/smile_plz12"))

# Show the latest Log file or a specified Log File
@app.route('/log',methods=['GET'])
@app.route('/log/<datelog>',methods=['GET'])
def show_logs(datelog=None):
  log_date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5,minutes=30)))
  if datelog in (log_date.strftime('%d_%m_%y'),"latest") or datelog is None:
    try:
      log_file = open(f"Logs/log_{log_date.strftime('%d_%m_%y')}.txt","r",encoding="utf-8")
      log_date_formatted = log_date.strftime('%d/%m/%y (Latest)') 
    except FileNotFoundError:
      log_file = open(f"Logs/log_{(log_date-datetime.timedelta(days=1)).strftime('%d_%m_%y')}.txt","r",encoding="utf-8")
      log_date_formatted = (log_date-datetime.timedelta(days=1)).strftime('%d/%m/%y (Previous Day)')
  else:
    if not os.path.isfile(f"Logs/log_{datelog}.txt"):
        return abort(404)
    log_file = open(f"Logs/log_{datelog}.txt","r",encoding="utf-8")
    log_date_formatted = datelog.replace('_','/')+" (Old)"
  log_file_lines = log_file.readlines()
  log_file.close()
  final_list = calculate_sessions(log_file_lines)
  return render_template("log.html",log_list=final_list,log_date=log_date_formatted)

# Main Route For Downloading Log Files
@app.route('/log/download',methods = ['GET'])
@app.route('/log/download/<path:fname>',methods=['GET'])
def retfile(fname=None):
    latest_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5,minutes=30)))
    if fname == "latest" or fname is None:
      log_latest = f"Logs/log_{latest_time.strftime('%d_%m_%y')}.txt"
      if not os.path.isfile(log_latest):
          log_latest = f"Logs/log_{(latest_time-datetime.timedelta(days=1)).strftime('%d_%m_%y')}.txt"
      return send_file(log_latest, as_attachment=True)
    if not os.path.isfile(f"Logs/log_{fname}.txt"):
        return abort(404)   
    return send_file(f"Logs/log_{fname}.txt",as_attachment=True)

# Async Route For Fetching Summary
@app.route('/log_summary',methods=['GET'])
def get_summary():
    log_file = open(f"Logs/log_{request.headers['logdate'].split(' ')[1].replace('/','_')}.txt","r",encoding="utf-8")
    log_file_lines = log_file.readlines()
    log_file.close()
    final_list = calculate_sessions(log_file_lines)
    summary  = calculate_summary(final_list)
    return render_template("summary.html",summary=summary)

# Async Route for returning Log List
@app.route('/log_all_list',methods=['GET'])
def log_all_list():
  return render_template("loglist.html",logs_all=get_all()) 

# For running the Flask application
def run():
  port = int(os.environ.get("PORT", 8080))
  host = os.environ.get("HOST","localhost")
  app.run(host=host, port=port)

# Run in a separate thread for running multiple processes
def keep_alive():
  server = Thread(target=run)
  server.start()

if __name__ == '__main__':
  app.debug = True
  run()