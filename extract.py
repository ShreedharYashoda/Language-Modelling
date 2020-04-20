# -*- coding: utf-8 -*-
"""
@author: Shreedhar Yashoda

"""
import json
import pandas as pd
import re
import numpy as np
import string
pd.options.mode.chained_assignment = None
from utils import *
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

chunk = pd.read_csv('/path/to/your/downloaded/dataset.csv', chunksize=516000)
df = next(chunk)

df['text'] = get_text(df.message, 15)

df = df[['text']]

df['text'] = df['text'].apply(str)
df['text'] = df['text'].apply(extract)

df = df.replace(to_replace='None', value=np.nan).dropna()

df['text'] = df['text'].apply(rm_slash_t)
df['text'] = df['text'].apply(rm_emailid)
df['text'] = df['text'].apply(rm_date)
df['text'] = df['text'].apply(rm_time)
df['text'] = df['text'].apply(rm_digit)
df['text'] = df['text'].apply(rm_url)
df['text'] = df['text'].apply(rm_symbols)
df['text'] = df['text'].apply(rm_slash)
df['text'] = df['text'].apply(rm_file_name)
df['text'] = df['text'].apply(rm_tab)
df['text'] = df['text'].apply(rm_colon_word)
df['text'] = df['text'].apply(rm_colon)
df['text'] = df['text'].apply(rm_spaces)

df['text'] = df['text'].apply(remove_ent)  
df['text'] = df['text'].apply(remove_ent)
df['text'] = df['text'].apply(remove_ent)  # To remove the entities missed in the previous runs.


df = df[df.text != 'Thanks']  
df.dropna
df.to_csv('entities_removed2.csv', index= False)