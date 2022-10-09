import os
import re
import string
import nltk

import pandas as pd

from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

STOP_WORDS = stopwords.words()
CONTEXT_WORDS = ["loved","make","find", "enjoy", "stories","kindle","books","book","story","read","author","reading", "reads", "readings", "writer", "characters", "character", "authors" ,"series"]

# removing the emojies
# https://www.kaggle.com/alankritamishra/covid-19-tweet-sentiment-analysis#Sentiment-analysis
EMOJI_PATTERN = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)

#cleaning the text
def cleaning(text):
    """
    Convert to lowercase.
    Rremove URL links, special characters and punctuation.
    Tokenize and remove stop words.
    """
    text = text.lower()
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('[’“”…]', '', text)

    text = EMOJI_PATTERN.sub(r'', text)

    # removing the stop-words
    text_tokens = word_tokenize(text)
    tokens_without_sw = [word for word in text_tokens if (not word in STOP_WORDS) and (not word in CONTEXT_WORDS)]
    filtered_sentence = (" ").join(tokens_without_sw)
    text = filtered_sentence

    return text


max_rows = 98261  # 'None' to read whole file, 98261 is 10% of the number of rows of the original dataset before matching
data_set = "Kindle_Store_5.json"
directory = "../datasets"
path = os.path.join(directory, data_set)
df = pd.read_json(path, lines=True, nrows= max_rows)


dt = df['reviewText'].apply(cleaning)

word_count = Counter(" ".join(dt).split()).most_common(10)
word_frequency = pd.DataFrame(word_count, columns = ['Word', 'Frequency'])
print(word_frequency)