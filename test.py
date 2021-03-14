
from torch import nn
import torchtext
import torch

import nltk
from nltk import sent_tokenize 
from nltk import word_tokenize
from nltk import PorterStemmer
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import TweetTokenizer
# from sklearn.feature_extraction.text import CountVectorizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os


class NLP_model(nn.Module):
    def __init__(self, vocab, emb_size, num_classes):
        super().__init__()
        self.num_words = len(vocab)
        self.emb_size = emb_size
        self.emb = nn.Embedding(self.num_words, self.emb_size)
        self.emb.from_pretrained(vocab.vectors)
        self.lstm = nn.LSTM(input_size = emb_size, hidden_size = 32, batch_first = True, num_layers = 2)
        self.relu = nn.ReLU()
        self.lin = nn.Linear(64, num_classes)
        
    def forward(self, batch_data):
        token_embs = self.emb(batch_data)
        outputs, (h_n, c_n) = self.lstm(token_embs)
        
        last_hidden_state = h_n
        last_hidden_state = last_hidden_state.permute(1, 0, 2)
        last_hidden_state = last_hidden_state.flatten(start_dim = 1)

        last_hidden_state = self.relu(last_hidden_state)
        logits = self.lin(last_hidden_state)
        
        return logits
        
from collections import Counter
class Merger():
    
    def __init__(self, csv_path, max_length):
        glove = torchtext.vocab.GloVe(name='6B',dim=50)
        self.dataframe = pd.read_csv(csv_path)
        self.max_length = max_length
        self.label_dict = {
            "hate speech" : 0,
            "offensive language" : 1,
            "other": 2
        }
        self.dataframe['tweet_token'] = self.dataframe['tweet'].apply(lambda x: word_tokenize(x))
        
        all_mentioned_words = []
        for words in self.dataframe['tweet_token']:
            all_mentioned_words += words
        frequency = Counter(all_mentioned_words)
        self.vocab = torchtext.vocab.Vocab(counter = frequency, min_freq = 25, vectors = glove)
        
        
#         print(self.dataframe.head())

    def __len__(self):
        return len(self.dataframe['tweet'])
    
    def back_to_text(self, tokens):
        text = ''
        for tok in tokens:
            text += self.vocab.itos[tok] + " "
        return text
    
    
    def __getitem__(self, index):
        label = self.label_dict[self.dataframe['class'][index]]
        label = torch.tensor(label)
        int_tokens = []
        tweet_tokens = self.dataframe['tweet_token'][index]
        for token in tweet_tokens:
            int_tokens.append(self.vocab[token])
        if(len(int_tokens) < self.max_length):
            num_to_pad = self.max_length - len(int_tokens)
            int_tokens += [0] * num_to_pad
        else:
            int_tokens = int_tokens[:self.max_length]
        int_tokens = torch.tensor(int_tokens)
        return(int_tokens, label)

    def word_tokens_to_tensor(self, word_tokens):
        int_tokens=[]
        for token in word_tokens:
            int_tokens.append(self.vocab[token])
        if(len(int_tokens) < self.max_length):
            num_to_pad = self.max_length - len(int_tokens)
            int_tokens += [0] * num_to_pad
        else:
            int_tokens = int_tokens[:self.max_length]
        int_tokens = torch.tensor(int_tokens)
        int_tokens = int_tokens.unsqueeze(0)
        return int_tokens

    def preprocess_input(self, text):
        text = text.lower()
        tokens = word_tokenize(text)
        return tokens

sample = "Hello World this is Hackmerced"
dataset = Merger( './new_data.csv', 50)
word_tokens = dataset.preprocess_input(sample)
tokens = dataset.word_tokens_to_tensor(word_tokens)
# print(sample)
# print(word_tokens)
# print(tokens)
# print(tokens.shape)
# print(dataset.back_to_text(tokens))
model = NLP_model(vocab = dataset.vocab, emb_size = 50, num_classes = 3)
params_loaded = torch.load('my_model_weights.pt')
print(model.load_state_dict(params_loaded))
preds = model(tokens).squeeze()
print(preds.shape)
print(preds)
softmaxed_preds = preds.softmax()
class_pred = softmaxed_preds.argmax()
print(softmaxed_preds)
print(class_pred)
print(dataset.label_dict[class_pred])