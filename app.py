import os
from flask import Flask,render_template
from dotenv import load_dotenv

app = Flask(__name__,template_folder='templates',static_folder='static')
load_dotenv()

@app.route('/')
def index():
    return render_template("index.html",profile=os.environ.get("twitter_profile"))

def main():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0',port=port,debug=False)

if __name__=="__main__":
    main()