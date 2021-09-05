import os
from replit import db

# Load the log files in the filesystem from db
def load_files():
  """
  First delete the present log files in the Logs directory
  then load the data from replit db and save it in log files.
  """
  for log in os.listdir('Logs'):
    file_t = os.path.join('Logs',log)
    os.remove(file_t)
  for key in db.keys():
    log_t = "Logs/"+key+".txt" 
    log_file = open(log_t,'w')
    log_file.write(db[key])    

# Save the current data from the log file in the db
def save_file(curr):
  log_data = open(curr,'r')
  db[curr.split('/')[1].split('.')[0]] = log_data.read()

# Delete the specified log from db (only maintains last 14 days)   
def clean_db(del_date):
  key_del = del_date.split('/')[1].split('.')[0]
  del db[key_del]