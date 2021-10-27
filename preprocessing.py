from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import text_to_word_sequence
from keras.preprocessing.text import Tokenizer
from tensorflow.keras import preprocessing
from tensorflow import keras
import tensorflow as tf
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os
import re
import shutil
import string
import json
import random
import numpy as np

import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


def remove_emojis(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    return text


def break_attached_words(sentence):
    s = sentence.split()
    for i in range(len(s)):
        if len(s[i]) == 1 or s[i].islower() or s[i].isupper():
            pass
        else:
            temp = []
            start = 0
            for j in range(1, len(s[i])):
                if s[i][j].isupper():
                    temp.append(s[i][start:j])
                    start = j
            temp.append(s[i][start:])
            s[i] = ' '.join(temp)
    return ' '.join(s)


def contractions_cleaning(sentence):
    with open('./resources/contractions.json') as f:
        contractions_dict = json.load(f)
    return ' '.join([contractions_dict.get(word, word) for word in sentence.split()])


def remove_stopwords(sentence):
    stop_words = set(stopwords.words('english'))
    return ' '.join([word for word in sentence.split() if not word in stop_words])


def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].lower()
    tag_dict = {"a": wordnet.ADJ,
                "n": wordnet.NOUN,
                "v": wordnet.VERB,
                "r": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)


def lemmatize_sentence(sentence):
    lemmatizer = WordNetLemmatizer()
    sentence = ' '.join([lemmatizer.lemmatize(w, get_wordnet_pos(w))
                         for w in sentence.split()])
    return sentence


def preprocess_text(input):
    # Remove emojis
    clean_sentence = ' '.join([word for word in remove_emojis(input).split()])

    # Replace annoying apostrophe
    clean_sentence = clean_sentence.replace("’", "'")

    # Replace ampersand with "and"
    clean_sentence = clean_sentence.replace('&amp;', 'and')

    # Remove numbers
    clean_sentence = re.sub(r"\d+", "", clean_sentence)

    # Remove punctuation
    clean_sentence = ' '.join([word.strip(string.punctuation)
                               for word in clean_sentence.split()])

    # Break attached words
    clean_sentence = break_attached_words(clean_sentence)

    # Convert tweets into lowercase
    clean_sentence = clean_sentence.lower()

    # Expand contractions
    clean_sentence = contractions_cleaning(clean_sentence)

    # Ensure only alphanumeric
    clean_sentence = re.sub(r"[^A-Za-z0-9]", " ", clean_sentence)

    # Remove stopwords
    clean_sentence = remove_stopwords(clean_sentence)

    # Lemmatization
    clean_sentence = lemmatize_sentence(clean_sentence)

    return clean_sentence
