import re
import random

#When tweet is longer than 280 chars
def tweet_with_repl(api,q1,q2):
    q1 = q1[:280]
    q2 = q2[:280]
    t1 = api.update_status(status=q1,tweet_mode="extended")
    if len(q2)<30:
      return t1,None
    t2 = api.update_status(status=q2,in_reply_to_status_id=t1.id,auto_populate_reply_metadata=True,tweet_mode="extended")
    return t1,t2

# Divide tweet for tweeting 
def partition_quote(quote):
    pattern = re.compile(r"^(.{250}[^\.\,\;\:\-\_\n\#\!\@\$\%\^\&\*\(\)\{\}\[\]\\\/\?\<\>\'\"\|\+\—\–\·\°\✓\•]*)(.*)",re.S)
    quote_re = re.search(pattern,quote)
    return quote_re

# Default tweet method   
def tweet_quote(api,quote):
    append_to_s1 = (",",".",";",":",")","}","]","?","!","|","'","\"","—","–","·","°","✓","•")
    if len(quote)<278:
      tweet = api.update_status(quote,tweet_mode="extended")
      return tweet,None
    quote_re = partition_quote(quote)
    if quote_re is None:
      s1_quote = quote[:274]+" (1/2)"
      s2_quote = quote[274:]+" (2/2)"
    else: 
      if len(quote_re.groups())<2:
        s1_quote = quote_re.group(1)+" (1/2)"
        s2_quote = quote.replace(s1_quote,"")+" (2/2)"
      else:
        s1_quote,s2_quote = quote_re.groups()
        f_char = s2_quote[:1] 
        if f_char in append_to_s1:
          s1_quote+=f_char
          s2_quote=s2_quote[1:]
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
    if len(quote+to_add)<278:
      tweet = api.update_status(quote+to_add,tweet_mode="extended")
      return tweet,None    
    quote +=to_add  
    quote_re = partition_quote(quote)
    if quote_re is None:
      s1_quote = quote[:272]+" (1/2)"
      s2_quote = quote[272:]+" (2/2)"
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
