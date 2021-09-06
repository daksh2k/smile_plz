import re
import random
import datetime
from time import sleep
from bson import ObjectId

# Return current date and time in a specific format for logging
def current_time():
  return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5,minutes=30))).strftime('[%d/%b/%Y %I:%M:%S %p] ')

#Return quote with proper formatting for logging 
def print_quote(qt):
  qt_list = qt.split('\n')
  qt_list = [f"{current_time()}Line {i+1}: {line}" for i,line in enumerate(qt_list)]
  return '\n'.join(qt_list)
  
#Update tweetcount in quotes DB
def update_count(doc,coll):
    """
    Update the tcount parameter of the quote/doc used for tweeting
    so it does not get used again.
    """
    new_value = {'$inc' :{'tcount' : 1}}
    coll.update_one({'_id': ObjectId(doc["_id"])},new_value)
    print(f"{current_time()}Successfully updated in DB!")  

# Parse and format the tags to be included in the quote
def parse_tags(tags_to_parse):
    """
    Get the different tags by splitting the string from the tags string.
    Remove spaces and replace "-" with "_" which is twitter friendly for hashtags.
    
    Randomly choose 3 tags which are between 3 and 15 chars and
    match the regex, which checks if the tag is valid on twitter.
    See https://regex101.com/r/CYZroW/2 for regex details.
    
    If no tags are less than 15 chars then randomly add 2 tags matching the regex.
    Always add the #quotes tag at the starting, then add the rest of the tags.
    """
    tags_list = [tag.strip().replace(" ","").replace("-","_") for tag in tags_to_parse.strip().split(',') if tag.strip().replace(" ","").replace("-","_")!=""]
    tags_list = random.sample(tags_list,len(tags_list))
    tags_list_final = []
    for tag in tags_list:
        if len(tags_list_final)==3:
            break
        if re.match(r"^(?=.{3,15}$)^(\w*[a-zA-Z]+\w*)$",tag) is not None:
           tags_list_final.append(tag)
    if len(tags_list_final)<2:
        for tag in tags_list:
          if len(tags_list_final)==2:
             break
          if re.match(r"^(?=.{2,}$)^(\w*[a-zA-Z]+\w*)$",tag) is not None:
             tags_list_final.append(tag)
    tags = "\n#quotes #"+" #".join(tags_list_final)
    if tags[-2:]==" #":
        tags = tags[:-2]
    return tags

#Parse the document and return with proper formatting
def parse_doc(doc):
    """
    :param doc["text"]: The main text of quote. Add it directly to the quote.
    
    :param doc["author"]: The author of the quote which sometimes also contains source of the quote
    so only add the author part to the quote first.
    
    :param doc["author"](Optional Source): Check if it contains the source
    Only add it to quote if it's length does not exceed 550 chars after adding.
    
    :param doc["tags"](Optional Tags): The relevant tags of the quote.
    Parse it using parse_tags to convert it to a twitter friendly format
    Only add it to quote if it's length does not exceed 550 chars after adding.
    """
    quote  = doc["text"].strip()
    auth = doc["author"].strip().split(',')[0]
    quote += "\n–"+auth.strip() 
    try:
      source_all = doc["author"].strip().split(",")
      source = ""
      for i in range(1,len(source_all)):
        source +=source_all[i].strip()
      if len(quote+source)<550 and source!="":
        quote+=f" ({source})"
    except IndexError:
      pass
    tags = parse_tags(doc["tags"])
    if len(quote+tags)<550:
      quote += tags
    print(f"{current_time()}Returned quote from DB-:\n{quote}")
    return quote

#Get quote from a very large dataset(Around 500k) 
def main(client):
    """
    Use the aggregate function of MongoDB to get a document/quote
    from db. The aggregate function gets a random quote from the db which has
    the parameter tcount=0 i.e the quote which has not been used before.

    If the quote after parsing and formatting is larger than 560 chars
    i.e. not able to tweet even after dividing in 2 parts
    then get again recursively till it is less than 560 chars
    """
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
        sleep(2)
        print(f"{current_time()}Very long quote! {len(quote)} words\n{current_time()}Getting again!")
        return main(client)
    return quote  