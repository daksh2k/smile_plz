import os
from replit import db

def load_files():
  for log in os.listdir('Logs'):
    file_t = os.path.join('Logs',log)
    os.remove(file_t)
  for key in db.keys():
    log_t = "Logs/"+key+".txt" 
    log_file = open(log_t,'w')
    log_file.write(db[key])    

def save_file(curr):
  log_data = open(curr,'r')
  db[curr.split('/')[1].split('.')[0]] = log_data.read()

# def save_file():
#   for log in os.listdir('Logs'):
#     file_t = os.path.join('Logs',log)
#     log_data = open(file_t,'r')
#     db[os.path.splitext(log)[0]] = log_data.read()

def clean_db(del_date):
  key_del = del_date.split('/')[1].split('.')[0]
  del db[key_del]