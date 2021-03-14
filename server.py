from flask import Flask, request, Response
import os
import torch


app = Flask(__name__)

# def runModel():
#     model = nlpmodel
#     params_loaded = torch.load('my_model_weights.pt')

#     model2.load_state_dict(params_loaded)

@app.route("/")
def index():
    return "hi"
   