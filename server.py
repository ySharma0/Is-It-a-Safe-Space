from flask import Flask, request, Response, render_template, redirect
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import os
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATBASE_URL is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# setup selenium chrome
# options = webdriver.ChromeOptions()
# options.binary_location = "/app/.apt/usr/bin/google-chrome-stable"
# options.add_argument("--headless")
# driver = webdriver.Chrome(chrome_options=options)

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
    return render_template("index.html")
   
@app.route("/getData")
def getData():
    url = str(request.values.get("url"))
    
    if re.match(regex, url) is not None:
        x = db.execute("select type, freq from urls where url='"+url+"';").fetchone()
        if x:
            
        # driver.get(url)
        # soup = BeautifulSoup(driver.page_source.encode("utf-8"), "lxml") # grab text
        # #clean text
        # soup = os.linesep.join([s for s in soup.text.splitlines() if s])
        # soup = soup.split("\n")
        
        # #push url to db
        # classification = "safe"
        # db.execute("INSERT INTO urls VALUES(:url, :type, :freq)",{"url":url, "type": classification, "freq": 1})
        # db.commit()
        

        return str("Badly Formatted URL")
    else:
        return url
         


