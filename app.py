import os
from flask import Flask,render_template
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

@app.route('/')
def index():
    return render_template("index.html",profile=os.environ.get("twitter_profile","https://twitter.com/smile_plz12"))

def main():
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST","0.0.0.0")
    app.run(host=host,port=port,debug=False)

if __name__=="__main__":
    main()