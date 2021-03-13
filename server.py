from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup
import re
from selenium import webdriver
# import os
# from sqlalchemy import create_engine, exc
# from sqlalchemy.orm import scoped_session, sessionmaker


regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

app = Flask(__name__)
@app.route("/")
def index():
    return ("hello")
   
@app.route("/getData")
def getData():
    url = str(request.values.get("url"))
    if re.match(regex, url) is not None:
        options = ChromeOptions()
        options.binary_location = "/app/.apt/usr/bin/google-chrome-stable"
        driver = webdriver.Chrome(chrome_options=options)
        # soup = BeautifulSoup(results.html.html, "lxml")
        return str("hi")
        # return url
    else:
        return "badly formatted url"

   