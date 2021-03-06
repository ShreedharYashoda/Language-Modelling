import string
import re
import json
import tensorflow as tf
import collections
import os

remove = string.punctuation
remove = remove.replace(":", "") # don't remove colons
pattern = r"[{}]".format(remove) # create the pattern

def rm_symbols(s):
  s = ''.join(re.sub(pattern, "", s))       
  return s

def rm_slash_t(s):
  s = ''.join(re.sub(r'\t','',s))       
  return s

def rm_colon_word(s):
  s = ''.join(re.sub(r'[A-Za-z0-9][A-Za-z0-9. ]*:','',s))       
  return s

def rm_colon(s):
  s = ''.join(re.sub(r':','',s))       
  return s

def rm_emailid(s):
  s = ''.join(re.sub(r'\S*@\S*\s?','',s))       
  return s

def rm_date(s):
  s = ''.join(re.sub(r'[0-9]{2}[\/,:][0-9]{2}[\/,:][0-9]{2,4}','',s))        
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

def rm_spaces(s):
  s = ' '.join(s.split())
  return s

def rm_tab(s):
  s = ''.join(re.sub(r'\S*\\S*\s?','',s))   
  return s
  
def rm_slash(s):
  s = ''.join(re.sub(r'\S*/\S*\s?','',s))   
  return s

def remove_ent(s):
  doc = nlp(s)
  print(type(doc))
  print([(X.text, X.label_) for X in doc.ents])
  text_no_namedentities = ""
  for token in doc:
    if not token.ent_type:
      text_no_namedentities += token.text
      if token.whitespace_:
        text_no_namedentities += " "
  return text_no_namedentities

def get_text(Series, row_num_slicer):
    """returns a Series with text sliced from a list split from each message. Row_num_slicer
    tells function where to slice split text to find only the body of the message."""
    result = pd.Series(index=Series.index)
    for row, message in enumerate(Series):
        message_words = message.split('\n')
        del message_words[:row_num_slicer]
        result.iloc[row] = message_words
    return result

def extract(st):
  match = re.search('Subject:(.+?)Thanks',st)
  if match:
    st = st[match.start():match.end()]
    return st
  else:
    return None

def read_words(filename):
    with tf.io.gfile.GFile(filename, 'r') as f:
        return f.read().replace('\n', '<eos>').split()

def load_dict(path):
  return json.loads(open(path).read())

def build_vocab(filename):
    data = read_words(filename)
    counter = collections.Counter(data)
    count_pairs = sorted(counter.items(), key=lambda x: (-x[1], x[0]))
    words, _ = list(zip(*count_pairs))
    word_to_id = dict(zip(words, range(len(words))))

    return word_to_id


def file_to_word_ids(filename, word_to_id):
    data = read_words(filename)
    return [word_to_id[word] for word in data if word in word_to_id]


def load_data():
    train_path = os.path.join(data_path, 'ptb.train.txt')
    valid_path = os.path.join(data_path, 'ptb.valid.txt')

    word_to_id = build_vocab(train_path)
    train_data = file_to_word_ids(train_path, word_to_id)
    valid_data = file_to_word_ids(valid_path, word_to_id)
    total_words = len(word_to_id)
    reversed_dictionary = dict(zip(word_to_id.values(), word_to_id.keys()))
    dictionary = {value: key for key, value in reversed_dictionary.items()}

    print('\ntotalwords : ', total_words, '\n')
    return train_data, valid_data, total_words, reversed_dictionary, dictionary


def save_json(dictionary, filename):
    with open(filename, 'w') as fp:
        json.dump(dictionary, fp)

class BatchGenerator(object):

    def __init__(self, data, num_steps, batch_size, total_words, skip_step=5):
        self.data = data
        self.num_steps = num_steps
        self.batch_size = batch_size
        self.total_words = total_words
        self.current_idx = 0
        self.skip_step = skip_step

    def generate(self):
        x = np.zeros((self.batch_size, self.num_steps))
        y = np.zeros((self.batch_size, self.num_steps, self.total_words))
        while True:
            for i in range(self.batch_size):
                if self.current_idx + self.num_steps >= len(self.data):
                    self.current_idx = 0
                x[i, :] = self.data[self.current_idx:self.current_idx + self.num_steps]
                temp_y = self.data[self.current_idx +
                                   1:self.current_idx + self.num_steps + 1]
                y[i, :, :] = tf.keras.utils.to_categorical(
                    temp_y, num_classes=self.total_words)
                self.current_idx += self.skip_step
            yield x, y


