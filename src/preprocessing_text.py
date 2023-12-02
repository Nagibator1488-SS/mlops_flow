import re

import numpy as np
from pymystem3 import Mystem


def remove_emoji(string):
    emoji_pattern = re.compile("["u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u'\U00010000-\U0010ffff'
                               u"\u200d"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\u3030"
                               u"\ufe0f"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def remove_links(string):
    string = re.sub(r'http\S+', '', string)  # remove http links
    string = re.sub(r'bit.ly/\S+', '', string)  # rempve bitly links
    string = re.sub(r'www\S+', '', string)  # rempve bitly links
    string = string.strip('[link]')  # remove [links]
    return string


def preprocessing(string, stopwords, stem):
    string = remove_emoji(string)
    string = remove_links(string)

    string = re.sub('(((?![а-яА-Я ]).)+)', ' ', string)
    string = ' '.join([
        re.sub('\\n', '', ' '.join(stem.lemmatize(s))).strip()
        for s in string.split()
    ])
    string = ' '.join([s for s in string.split() if s not in stopwords])
    return string


def get_clean_text(data, stopwords):
    stem = Mystem()
    comments = [preprocessing(x, stopwords, stem) for x in data]
    return comments


def vectorize_text(data, tfidf):
    return tfidf.transform(data).toarray()
