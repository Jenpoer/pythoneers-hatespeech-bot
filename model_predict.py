import pickle

import numpy as np

import tensorflow as tf
from tensorflow.keras import preprocessing
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.text import text_to_word_sequence
from keras.preprocessing.sequence import pad_sequences

from preprocessing import preprocess_text


def load_model():
    model = tf.keras.models.load_model('./model/im_rnn_model_gru_75f1.h5')
    return model

def predict(input):
    clean_text = preprocess_text(input)
    with open('./resources/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    seq = tokenizer.texts_to_sequences([clean_text])
    test_sentence = pad_sequences(seq, maxlen=64)

    model = load_model()
    prediction = model.predict(test_sentence)
    predicted_class = np.where(prediction > 0.5, 1, 0).flatten()
    return predicted_class[0]