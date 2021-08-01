from flask import Flask,render_template,url_for,abort,send_file,redirect
from threading import Thread
import datetime
import os
app = Flask('',template_folder='static')
app.debug = True

@app.route('/',methods=['GET'])
def main():
  return render_template("index.html",profile=os.environ.get("twitter_profile"))
  
@app.route('/log',methods=['GET'])
def show_logs():
  log_date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5,minutes=30)))
  try:
     try:
        not_found=0
        log_file = open(f"Logs/log_{log_date.strftime('%d_%m_%y')}.txt","r",encoding="utf-8")
     except FileNotFoundError:
        not_found=1
        log_file = open(f"Logs/log_{(log_date-datetime.timedelta(days=1)).strftime('%d_%m_%y')}.txt","r",encoding="utf-8")  
     log_file_lines = log_file.readlines()
     log_file.close()
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
     if not_found:
        return render_template("log.html",log_list=final_list,log_date=(log_date-datetime.timedelta(days=1)).strftime('%d/%m/%Y (Previous Day)'),dl_href="log/download/latest")
     return render_template("log.html",log_list=final_list,log_date=log_date.strftime('%d/%m/%Y (Latest)'),dl_href="log/download/latest")
  except Exception as e:
     return e     

@app.route('/log/<datelog>',methods=['GET'])
def retlog(datelog):
     if not os.path.isfile(f"Logs/log_{datelog}.txt"):
        return abort(404)
     log_file = open(f"Logs/log_{datelog}.txt","r",encoding="utf-8")
     log_file_lines = log_file.readlines()
     log_file.close()
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
     return render_template("log.html",log_list=final_list,log_date=datelog.replace('_','/')+" (Old)",dl_href=f"download/{datelog}") 

@app.route('/log/download',methods=['GET'])
def download():
    return redirect('/log/download/latest',code=303)

@app.route('/log/download/<path:fname>',methods=['GET'])
def retfile(fname):
    latest_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5,minutes=30)))
    if fname in ("/","latest"):
      log_latest = f"Logs/log_{latest_time.strftime('%d_%m_%y')}.txt"
      if not os.path.isfile(log_latest):
          log_latest = f"Logs/log_{(latest_time-datetime.timedelta(days=1)).strftime('%d_%m_%y')}.txt"
      return send_file(log_latest, as_attachment=True)
    if not os.path.isfile(f"Logs/log_{fname}.txt"):
        return abort(404)   
    return send_file(f"Logs/log_{fname}.txt",as_attachment=True)

def run():
  app.run(host="localhost", port=8080)
  app.add_url_rule('/favicon.ico',redirect_to=url_for('static', filename='favicon.ico'))

def keep_alive():
  server = Thread(target=run)
  server.start()

if __name__ == '__main__':
    run()