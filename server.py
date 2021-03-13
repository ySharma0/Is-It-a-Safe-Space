from flask import Flask, request
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re


# from sqlalchemy import create_engine, exc
# from sqlalchemy.orm import scoped_session, sessionmaker
import os


app = Flask(__name__)
session = HTMLSession()
regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

@app.route("/")
def index():
    return ("hello")
   

@app.route("/getData")
def getData():
    url = str(request.values.get("url"))
    if re.match(regex, url) is not None:
        resp = session.get(url)
        resp.html.render()
        soup = BeautifulSoup(resp.html.html, "lxml")
        return soup.text
    else:
        return "badly formatted url"

   