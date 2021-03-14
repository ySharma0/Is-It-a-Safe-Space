from flask import Flask, request, Response, render_template, redirect, jsonify
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import os
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
os.system('pip install torch==1.8.0+cpu -f https://download.pytorch.org/whl/torch_stable.html')

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATBASE_URL is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# setup selenium chrome
options = webdriver.ChromeOptions()
options.binary_location = "/app/.apt/usr/bin/google-chrome-stable"
options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=options)

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



@app.route("/getData", methods=["GET", "POST"])
def getData():
    url = str(request.form.get("url"))
    print(url)
    if re.match(regex, url) is not None:
        x = db.execute("select type, freq from urls where url='"+url+"';").fetchone()
        if x:
            db.execute("UPDATE urls SET freq="+ str(x[1]+1) + "where url='"+url+"';")
            db.commit()
            return str(x[0])
            
        driver.get(url)
        soup = BeautifulSoup(driver.page_source.encode("utf-8"), "lxml") # grab text
        #clean text
        soup = os.linesep.join([s for s in soup.text.splitlines() if s])
        soup = soup.split("\n")
        
        #push url to db
        # 0 : hate speech    1 : profainity   2 : neither
        
        classification = "profanity"
        db.execute("INSERT INTO urls VALUES(:url, :type, :freq)",{"url":url, "type": classification, "freq": 1})
        db.commit()      

        return str(soup)
    else:
        return str("Badly Formatted URL")
         

@app.route("/getSafeSites")
def getSafeSites():
    x = db.execute("select url, freq from urls where type='safe' order by freq desc;").fetchall()
    return render_template("safePages.html", arr=x)

@app.route("/getDangerSites")
def getDangerSites():
    w = db.execute("select url, freq, type from urls where type='profanity' or type='hate' order by freq desc;").fetchall()
    return render_template("unsafePages.html", arr=w)

@app.route("/getAbout")
def getAbout():
    print("hi")
    return render_template("AboutUs.html")