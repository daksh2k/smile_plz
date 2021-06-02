import os
from flask import Flask,render_template,url_for

app = Flask(__name__,template_folder='static')

@app.route('/')
def index():
    return render_template("index.html")
def main():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0',port=port,debug=False)
    app.add_url_rule('/favicon.ico',redirect_to=url_for('static', filename='favicon.ico'))
if __name__=="__main__":
    main()