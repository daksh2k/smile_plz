from bson import ObjectId
from time import sleep
import random

#Update tweetcount in quotes DB
def update_count(doc,coll):
    new_value = {'$inc' :{'tcount' : 1}}
    coll.update_one({'_id': ObjectId(doc["_id"])},new_value)  

#Return the quote with proper formatting
def parse_doc(doc):
    tags_list = [tag.strip().replace(" ","").replace("-","_") for tag in doc["tags"].strip().split(',')]
    quote  = doc["text"].strip()
    auth = doc["author"].strip().split(',')[0]
    quote += "\n–"+auth.strip() 
    try:
      source = doc["author"].strip().split(',')[1]
      quote+=f" ({source.strip()})"
    except IndexError:
      pass
    tags_list = random.sample(tags_list,len(tags_list))
    tags_list_f = []
    for tag in tags_list:
        if len(tags_list_f)==3:
            break
        if len(tag)<15:
           tags_list_f.append(tag)    
    if not tags_list_f:
        for tag in tags_list:
          if len(tags_list_f)==2:
             break
          tags_list_f.append(tag)
    tags = "\n#quotes #"+" #".join(tags_list_f)
    if tags[-2:]==" #":
        tags = tags[:-2]
    quote += tags
    return quote

#Get quote from a very large dataset(Around 500k) 
def main(client):
    db = client.tweetbot
    coll = db.quotes500k
    for doc in coll.aggregate([{'$match' :{'tcount': 0}},{'$sample': {'size': 1}}]):
        try:
            quote = parse_doc(doc)
        except Exception as e:
            print(f"Error parsing doc/quote\n{e}")
            sleep(3)
            return main(client)     
        try: 
            update_count(doc,coll)
        except Exception as e:
            print(f"Error in Updating tcount in db\n{e}")
    if len(quote)>540:
        sleep(3)
        print(f"Very long quote! {len(quote)} words\n{quote}\nGetting again!")
        return main(client)
    return quote  