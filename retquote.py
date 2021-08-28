from bson import ObjectId
import re
from time import sleep
import random
import datetime

# Return Current Date and Time
def current_time():
  return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5,minutes=30))).strftime('[%d/%b/%Y %I:%M:%S %p] ')

#Print Quote With Proper Formatiing
def print_quote(qt):
  qt_list = qt.split('\n')
  qt_list = [f"{current_time()}Line {i+1}: {line}" for i,line in enumerate(qt_list)]
  return '\n'.join(qt_list)
  
#Update tweetcount in quotes DB
def update_count(doc,coll):
    new_value = {'$inc' :{'tcount' : 1}}
    coll.update_one({'_id': ObjectId(doc["_id"])},new_value)
    print(f"{current_time()}Successfully updated in DB!")  

#Return the quote with proper formatting
def parse_doc(doc):
    tags_list = [tag.strip().replace(" ","").replace("-","_") for tag in doc["tags"].strip().split(',') if tag.strip().replace(" ","").replace("-","_")!=""]
    quote  = doc["text"].strip()
    auth = doc["author"].strip().split(',')[0]
    quote += "\n–"+auth.strip() 
    try:
      source_all = doc["author"].strip().split(',')
      source = ""
      for i in range(1,len(source_all)):
        source +=source_all[i].strip()
      if len(quote+source)<550 and source!="":
        quote+=f" ({source})"
    except IndexError:
      pass
    tags_list = random.sample(tags_list,len(tags_list))
    tags_list_final = []
    for tag in tags_list:
        if len(tags_list_final)==3:
            break
        if re.match(r"^(?=.{3,15}$)^(\w*[a-zA-Z]+\w*)$",tag) is not None:
           tags_list_final.append(tag)    
    if not tags_list_final:
        for tag in tags_list:
          if len(tags_list_final)==2:
             break
          if re.match(r"^(?=.{2,}$)^(\w*[a-zA-Z]+\w*)$",tag) is not None:   
             tags_list_final.append(tag)
    tags = "\n#quotes #"+" #".join(tags_list_final)
    if tags[-2:]==" #":
        tags = tags[:-2]
    if len(quote+tags)<550:
      quote += tags
    print(f"{current_time()}Returned quote from DB-:\n{quote}")
    return quote

#Get quote from a very large dataset(Around 500k) 
def main(client):
    db = client.tweetbot
    coll = db.quotes500k
    for doc in coll.aggregate([{'$match' :{'tcount': 0}},{'$sample': {'size': 1}}]):
        try:
            quote = parse_doc(doc)
        except Exception as e:
            print(f"{current_time()}Error parsing doc quote\n{current_time()}{e}")
            sleep(3)
            return main(client)     
        try: 
            update_count(doc,coll)
        except Exception as e:
            print(f"{current_time()}Error in Updating tcount in db\n{current_time()}{e}")
    if len(quote)>560:
        sleep(3)
        print(f"{current_time()}Very long quote! {len(quote)} words\n{current_time()}Getting again!")
        return main(client)
    return quote  