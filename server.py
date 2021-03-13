from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
# from sqlalchemy import create_engine, exc
# from sqlalchemy.orm import scoped_session, sessionmaker
import os


app = Flask(__name__)

@app.route("/")
def index():
    return ("hello")
