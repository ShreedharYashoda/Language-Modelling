import string
import re

remove = string.punctuation
remove = remove.replace(":", "") # don't remove colons
pattern = r"[{}]".format(remove) # create the pattern

def rm_emailid(s):
  s = ''.join(re.sub(r'\S*@\S*\s?','',s))
  return s

def rm_symbols(s):
  s = ''.join(re.sub(pattern, "", s))
  return s

def rm_date(s):
  s = ''.join(re.sub(r'[0-9]{2}[\/,:][0-9]{2}[\/,:][0-9]{2,4}','',s))        #:(?=..(?<!\d:\d\d))|[^a-zA-Z0-9 ](?<!:)         ^(?:(?:[0-9]{2}[:\/,]){2}[0-9]{2,4}|am|pm)$
  return s

def rm_time(s):
  s = ''.join(re.sub(r'(1[0-2]|0?[1-9]):([0-5][0-9]) ([AaPp][Mm])','',s))
  return s

def rm_file_name(s):
  s = ''.join(re.sub(r'/[^\\]*\.(\w+)$/','',s))
  return s

def rm_digit(s):
  s = ''.join([i for i in s if not i.isdigit()])
  return s

def rm_url(s):
  s = ''.join(re.sub(r'http\S+','',s))
  return s
