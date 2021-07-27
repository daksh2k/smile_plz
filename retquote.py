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
    quote += "\n-"+auth.strip() 
    try:
      source = doc["author"].strip().split(',')[1]
      quote+=f" ({source.strip()})"
    except IndexError:
      pass
    if len(tags_list)>3:
        tags_list = random.sample(tags_list,3)
    tags = "\n#quotes #"+' #'.join(tags_list)
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