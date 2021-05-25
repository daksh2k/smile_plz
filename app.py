from flask import Flask,render_template,url_for
app = Flask(__name__,template_folder='static')

@app.route('/')
def index():
    return render_template("index.html")
if __name__=="__main__":
    app.run(debug=False)
    app.add_url_rule('/favicon.ico',
                 redirect_to=url_for('static', filename='favicon.ico'))
# app.run(host='0.0.0.0', port=5000)
#app.run(host='0.0.0.0', port=environ.get('PORT'))