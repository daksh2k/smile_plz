from os 
from flask import Flask
app = Flask(__name__)
app.run(host='0.0.0.0', port=5000)
#app.run(host='0.0.0.0', port=environ.get('PORT'))