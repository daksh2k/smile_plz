from flask import Flask,render_template,url_for
from threading import Thread
app = Flask('',template_folder='static')
@app.route('/')
def main():
  return render_template("index.html")
def run():
  app.run(host="0.0.0.0", port=8080)
  app.add_url_rule('/favicon.ico',redirect_to=url_for('static', filename='favicon.ico'))
def keep_alive():
  server = Thread(target=run)
  server.start()  