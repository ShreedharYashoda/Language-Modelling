import pandas as pd
import numpy as np
from utils import rm_url, rm_date, rm_time, rm_digit, rm_emailid, rm_symbols, rm_file_name
pd.options.mode.chained_assignment = None

def get_text(Series, row_num_slicer):
    """returns a Series with text sliced from a list split from each message. Row_num_slicer
    tells function where to slice split text to find only the body of the message."""
    result = pd.Series(index=Series.index)
    for row, message in enumerate(Series):
        message_words = message.split('\n')
        del message_words[:row_num_slicer]
        result.iloc[row] = message_words
    return result

chunk = pd.read_csv('emails.csv', chunksize=516000)
data = next(chunk)

data.info()

data['text'] = get_text(data.message, 15)

data = data[['text']]

#print(data.head())
