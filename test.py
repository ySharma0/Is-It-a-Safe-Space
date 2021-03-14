
# import pip3
# installed_packages = pip3.get_installed_distributions()
# installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
#      for i in installed_packages])
# print(installed_packages_list)
from torch import nn
import torch
class NLP_model(nn.Module):
    def __init__(self, num_words, emb_size, num_classes):
        super().__init__()
        self.num_words = num_words
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
def preprocess_input(text):
    print(text)
sample = "Hello World this is Hackmerced"
preprocess_input(sample)