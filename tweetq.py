import re
import random
from retquote import current_time

#When tweet is longer than 280 chars tweet with reply
def tweet_with_repl(api,q1,q2):
    try: 
      q1 = reduce_size(q1)
      q2 = reduce_size(q2)
    except:
      pass  
    if len(q2)<40:
      q1=q1[:280].strip()
    else:
      if len(q1)<275 and len(q2)<275:
        q1  +=" (1/2)"
        q2  +=" (2/2)"         
    t1 = api.update_status(status=q1[:280].strip(),tweet_mode="extended")
    if len(q2)<40:
      return t1,None
    t2 = api.update_status(status=q2[:280].strip(),in_reply_to_status_id=t1.id,auto_populate_reply_metadata=True,tweet_mode="extended")
    return t1,t2  

# Try reducing size by splitting and replacing
def reduce_size(qt):
    i=0
    split_char_list =  ("#","(","\n","\"","'",",",".")
    while len(qt)>280 and i<len(split_char_list):
        print(f"{current_time()}Tweet larger than 280 so replacing and reducing size! by {split_char_list[i]}")
        qt_split = qt.split(split_char_list[i])
        while len(qt_split)>1 and len(qt)>280:
             qt = qt.replace(qt_split[len(qt_split)-1],"")[:-1].strip()
             qt_split = qt.split(split_char_list[i])
        i+=1   
    return qt       

# Divide tweet for tweeting
def partition_quote(quote,words):
    pattern_string = r"^(.{"+str(words)+r"}[^\.\,\;\:\-\_\n\#\!\@\$\%\^\&\*\(\)\{\}\[\]\\\/\?\<\>\|\+\—\–\·\°\✓\•\"]*)(.*)"
    pattern = re.compile(pattern_string,re.S)
    quote_re = re.search(pattern,quote)
    return quote_re

# Partition again with less words if more than 280 chars 
def check_length(q1):
  if len(q1[0])<=280:
    print(f"{current_time()} Default partition!")
    return q1[0],q1[1]
  qg2 = partition_quote(q1[0],200)
  if qg2 is None:
    print(f"{current_time()} Default partition when 2nd partition failed!")
    return q1[0],q1[1]
  q2 = qg2.groups()
  if len(q1[1]+q2[1])<=280:
    print(f"{current_time()} 2nd partition successfull!")
    return q2[0],q2[1]+q1[1]
  sp_str = str(q2[1]+q1[1]).split("\n")
  print(f"{current_time()} 2nd partition successfull but second tweet not less than 280! So replacing last line!")
  return q2[0],str(q2[1]+q1[1]).replace(sp_str[len(sp_str)-1],"").strip()

# Default tweet method   
def tweet_quote(api,quote):
    append_to_s1 = (",",".",";",":",")","}","]","?","!","|","\"","·","°","✓","•")
    if len(quote)<=280:
      tweet = api.update_status(quote,tweet_mode="extended")
      return tweet,None
    quote_re = partition_quote(quote,250)
    if quote_re is None:
      s1_quote = quote[:280]
      s2_quote = quote[280:]
    else: 
      if len(quote_re.groups())<2:
        s1_quote = quote_re.group(1)
        s2_quote = quote.replace(s1_quote,"")
      else:
        s1_quote,s2_quote = check_length(quote_re.groups())
        s1_quote = s1_quote.strip()
        s2_quote = s2_quote.strip()
        f_char = s2_quote[:1] 
        if f_char in append_to_s1:
          s1_quote += f_char
          s2_quote  = s2_quote[1:].strip()
    print(f"{current_time()}Quote after partitioning: \n{current_time()}1st: {s1_quote}\n{current_time()}2nd: {s2_quote}")
    tweet,t2 = tweet_with_repl(api,s1_quote,s2_quote)
    return tweet,t2

#Tweet when db is down
def tweet_dbdown(api,quote):
    tags = ("#nature","#life","#wisdom","#happiness","#motivation","#inspiration","#laugh","#love","#wholesome","#cheerful",
      "#live","#smile","#inspire","#quoteoftheday","#thoughts","#quotesdaily","#quoteshourly","#lifequotes","#imagine","#quote",
      "#reality","#quotesoftheday","#happy","#successquotes","#quotestoliveby","#motivationalquotes","#mindset","#goals")
    if len(quote) >= 120:
      rand_tags = random.sample(tags,1)
    elif len(quote) <= 40:
      rand_tags = random.sample(tags,3)
    else:
      rand_tags = random.sample(tags,2)  
    to_add = "\n#quotes " + ' '.join(rand_tags)
    if len(quote+to_add)<=280:
      tweet = api.update_status(quote+to_add,tweet_mode="extended")
      return tweet,None    
    quote +=to_add  
    quote_re = partition_quote(quote,250)
    if quote_re is None:
      s1_quote = quote[:274]+" (1/2)"
      s2_quote = quote[274:]+" (2/2)"
    else: 
      if len(quote_re.groups())<2:
        s1_quote = quote_re.group(1)+" (1/2)"
        s2_quote = quote.replace(s1_quote,"")+" (2/2)"
      else:
        s1_quote,s2_quote = quote_re.groups()
        s1_quote +=" (1/2)"
        s2_quote +=" (2/2)"
    tweet,t2 = tweet_with_repl(api,s1_quote,s2_quote)
    return tweet,t2  
