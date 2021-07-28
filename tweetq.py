import re
import random

#When tweet is longer than 280 chars
def tweet_with_repl(api,q1,q2):
    try: 
      q1 = reduce_size(q1)
      q2 = reduce_size(q2)
    except:
      pass  
    t1 = api.update_status(status=q1[:280].strip(),tweet_mode="extended")
    if len(q2)<40:
      return t1,None
    t2 = api.update_status(status=q2[:280].strip(),in_reply_to_status_id=t1.id,auto_populate_reply_metadata=True,tweet_mode="extended")
    return t1,t2  

# Try reducing size by splitting and replacing
def reduce_size(qt,split_char="\n"):
    if len(qt)>280:
      try:
        qt_split = qt.split(split_char)
        if len(qt_split)>2:
           qt = qt.replace(qt_split[len(qt_split)-1],"").strip()
           return reduce_size(qt,split_char)
        elif len(qt)==2:
           qt = qt.replace(qt_split[1],"").strip()
           return reduce_size(qt,"(")
        return qt[:280].strip()    
      except Exception as e:
        print(f"Unable to reduce size!{e}")
        return qt[:280].strip()
    return qt       

# Divide tweet for tweeting 
def partition_quote(quote,words):
    pattern_string = r"^(.{"+str(words)+r"}[^\.\,\;\:\-\_\n\#\!\@\$\%\^\&\*\(\)\{\}\[\]\\\/\?\<\>\'\|\+\—\–\·\°\✓\•\"]*)(.*)"
    pattern = re.compile(pattern_string,re.S)
    quote_re = re.search(pattern,quote)
    return quote_re

# Check partition again if incorrect length 
def check_length(q1):
  if len(q1[0])<=280:
    return q1[0],q1[1]
  qg2 = partition_quote(q1[0],200)
  if qg2 is None:
    return q1[0],q1[1]
  q2 = qg2.groups()
  if len(q1[1]+q2[1])<=280:
    return q2[0],q2[1]+q1[1]
  sp_str = str(q2[1]+q1[1]).split("\n")
  return q2[0],str(q2[1]+q1[1]).replace(sp_str[len(sp_str)-1],"").strip()

# Default tweet method   
def tweet_quote(api,quote):
    append_to_s1 = (",",".",";",":",")","}","]","?","!","|","'","\"","·","°","✓","•")
    if len(quote)<=280:
      tweet = api.update_status(quote,tweet_mode="extended")
      return tweet,None
    quote_re = partition_quote(quote,250)
    if quote_re is None:
      s1_quote = quote[:274]+" (1/2)"
      s2_quote = quote[274:]+" (2/2)"
    else: 
      if len(quote_re.groups())<2:
        s1_quote = quote_re.group(1)+" (1/2)"
        s2_quote = quote.replace(s1_quote,"")+" (2/2)"
      else:
        s1_quote,s2_quote = check_length(quote_re.groups())
        s1_quote = s1_quote.strip()
        s2_quote = s2_quote.strip()
        f_char = s2_quote[:1] 
        if f_char in append_to_s1:
          s1_quote += f_char
          s2_quote  = s2_quote[1:].strip()
        s1_quote +=" (1/2)"
        s2_quote +=" (2/2)"
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
