import re
import random
from retquote import current_time

#When tweet is longer than 280 chars tweet with reply
def tweet_with_repl(api,q1,q2):
    """
    When first part is greater than 274 chars add the last words from the
    1st part to the starting of the 2nd part until it becomes less than 274.

    If the 2nd part is less than 30 chars then only tweet 1st part and return.
    Add part number at the end if tweeting both and no tweet exceeds 280 after adding.
    """
    replaced_words = []
    if len(q1)>274:
      split_by_space = q1.split(' ')
      print(f"{current_time()}Reducing size by adding words to second tweet!")
      while len(q1)>274 and len(split_by_space)>1:
         last_word = split_by_space.pop()
         replaced_words.append(last_word)
         q1 = q1[:-(len(last_word)+1)].strip()
         q2 = last_word + " " + q2
    if replaced_words:
      print(f"{current_time()}Words added to second Tweet: {', '.join(replaced_words)}")
    q1 = reduce_size(q1.strip())
    q2 = reduce_size(q2.strip()) 
    if len(q2)<30:
      q1=q1[:280].strip()
    else:
      if len(q1)<275 and len(q2)<275:
        q1  +=" (1/2)"
        q2  +=" (2/2)"         
    t1 = api.update_status(status=q1[:280].strip(),tweet_mode="extended")
    if len(q2)<30:
      return t1,None
    t2 = api.update_status(status=q2[:280].strip(),in_reply_to_status_id=t1.id,auto_populate_reply_metadata=True,tweet_mode="extended")
    return t1,t2  

# Try reducing size by splitting and replacing
def reduce_size(qt):
    """
    If everything fails and the tweet is longer than 280 chars
    then start removing stuff from the end by splitting the tweet
    and removing the end part till it becomes less than 280
    or reached the end of split char list i.e. no chars left to split with.
    """
    i=0
    split_char_list =  ("#","(","\n"," ",",",".","\"","'")
    while len(qt)>280 and i<len(split_char_list):
        s_char = "newline" if split_char_list[i]=="\n" else("space" if split_char_list[i]==" " else split_char_list[i])
        print(f"{current_time()}Tweet larger than 280 so replacing and reducing size by {s_char}")
        qt_split = qt.split(split_char_list[i])
        while len(qt_split)>1 and len(qt)>280:
             to_replace = qt_split.pop()
             qt = qt[:-(len(to_replace)+1)].strip()
        i+=1   
    return qt       

# Divide quote for tweeting
def partition_quote(quote,words):
    """
    Divide quote in 2 parts if it will not fit in 1 tweet.
    :param words: The minimum number of words for 1st part.
    See https://regex101.com/r/uZeBmC/1 for regex details.
    """
    pattern_string = r"^(.{"+str(words)+r"}[^\.\,\;\:\-\_\n\#\!\@\$\%\^\&\*\(\)\{\}\[\]\\\/\?\<\>\|\+\—\–\·\°\✓\•\"]*)(.*)"
    pattern = re.compile(pattern_string,re.S)
    quote_re = re.search(pattern,quote)
    return quote_re

# Partition again with less words if more than 280 chars 
def check_length(q1):
    """
    Return both parts as it is, if 1st part is less than 280 chars.
    If not try partitioning 1st part again with less words
    :return 1st part of 2nd partition
    :return 2nd part of 2nd partiton + 2nd part of 1st partition
    """
    if len(q1[0])<=280:
      if len(q1[1])<=280:
        print(f"{current_time()}Default partition! Both tweets less than 280!")
      else:
        print(f"{current_time()}Default partition! Second tweet greater than 280!")
      return q1[0].strip(),q1[1].strip()
    
    # If second partition fails
    quote_partition_2 = partition_quote(q1[0],200)
    if quote_partition_2 is None:
      if len(q1[1])<=280:
        print(f"{current_time()}Default partition! 2nd partition failed! First tweet greater than 280!")
      else:
        print(f"{current_time()}Default partition! 2nd partition failed! Both tweets greater than 280!")  
      return q1[0].strip(),q1[1].strip()
    
    # If only 1 part is returned by the regex
    q2 = quote_partition_2.groups()
    if len(q2)<2:
      if len(q1[1])<=280:
        print(f"{current_time()}Default partition! 2nd partition only returned 1 part! First tweet greater than 280!")
      else:
        print(f"{current_time()}Default partition! 2nd partition only returned 1 part! Both tweets greater than 280!")  
      return q1[0].strip(),q1[1].strip()
    
    # If 2 parts are returned by the regex
    if len(q2[0])<=280 and len(q1[1]+q2[1])<=280:
      print(f"{current_time()}2nd partition successfull! Both tweets less than 280!")
    elif len(q2[0])>280 and len(q1[1]+q2[1])<=280:
      print(f"{current_time()}2nd partition successfull! First tweet greater than 280!")
    elif len(q2[0])<=280 and len(q1[1]+q2[1])>280:
      print(f"{current_time()}2nd partition successfull! Second tweet greater than 280!")
    else:
      print(f"{current_time()}2nd partition successfull! Both tweets greater than 280!")
    return q2[0].strip(),(q2[1].strip()+" "+q1[1].strip()).strip()

# Parse when regex returns 2 valid groups
def parse_both_parts(quote):
    """
    Partition quote using partition_quote() and check if it returns
    2 valid parts, if not take the first 280 chars for part 1
    and rest for part 2.
    
    If partiton is sucessful return the 2 parts. 
    """
    quote_re = partition_quote(quote,250)
    if quote_re is None:
      s1_quote = quote[:280]
      s2_quote = quote[280:]
      print(f"{current_time()}Partition failed, no parts returned!")
    else: 
      if len(quote_re.groups())<2:
        s1_quote = quote_re.group(1)
        s2_quote = quote.replace(s1_quote,"")
        print(f"{current_time()}Partition failed, only 1 part returned!")
      else:
        append_to_s1 = (",",".",";",":",")","}","]","?","!","|","\"","·","°","✓","•")
        s1_quote,s2_quote = check_length(quote_re.groups())
        s1_quote = s1_quote.strip()
        s2_quote = s2_quote.strip()
        f_char = s2_quote[:1] 
        if f_char in append_to_s1:
          s1_quote += f_char
          s2_quote  = s2_quote[1:].strip()
    return s1_quote,s2_quote  

# Default tweet method when quote_method is db
def tweet_quote(api,quote):
    """
    If the quote is less than 280 chars tweet it and return, if not handle partitioning.

    Print/Log the both parts and send them to tweet.
    :return Both Status objects returned after tweeting. 
    """
    if len(quote)<=280:
      tweet = api.update_status(quote,tweet_mode="extended")
      return tweet,None
    
    # Handling when need to split in 2 parts
    s1_quote,s2_quote = parse_both_parts(quote)
    print(f"{current_time()}Quote after partitioning-:\n{current_time()}1st Part-:\n{s1_quote}\n{current_time()}2nd Part-:\n{s2_quote}")
    tweet,t2 = tweet_with_repl(api,s1_quote,s2_quote)
    return tweet,t2

#Default tweet method when quote_method is api
def tweet_dbdown(api,quote):
    """
    Add random tags when tweeting with api, according to the length of the tweet.
    If the quote is less than 280 chars tweet it and return, if not handle partitioning.
    
    Print/log the both parts and send them to tweet.
    :return Both Status objects returned after tweeting. 
    """
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
    
    # Handling when need to split in 2 parts
    quote +=to_add 
    s1_quote,s2_quote = parse_both_parts(quote)
    print(f"{current_time()}Quote after partitioning-:\n{current_time()}1st Part-:\n{s1_quote}\n{current_time()}2nd Part-:\n{s2_quote}")
    tweet,t2 = tweet_with_repl(api,s1_quote,s2_quote)
    return tweet,t2