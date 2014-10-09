from flask import Flask,render_template,request
from google import search
import urllib,pickle,re
from bs4 import BeautifulSoup
from collections import Counter
import operator
# this makes app an instance of the Flask class
# and it passed the special variable __name__ into
# the constructor

app = Flask(__name__)

h = open('diction.txt','rb')
d= pickle.load(h)
h.close()


def notname(lis):
    x=0
    for sub in lis:
        if sub in d:
            #print sub
            pass
            x=x+1
            #print x
        if x==2: 
            return True
    return False
def findnames(g):
    p = re.compile('(?:[A-Z][a-z].\.)* (?:[A-Z][a-z]+)(?:\s[A-Z][a-z]+)+')
    L=p.findall(g)
    x=0
    for i in xrange(len(L)):
        L[i] = L[i].replace('\n',' ')
        L[i] = L[i].lower().split(" ")
    #print stringify(L)

    L[:] = [ o for o in L if notname(o)==False]
    return L  



@app.route("/home", methods= ["GET", "POST"])
@app.route("/",methods= ["GET", "POST"]) 
def home():
    return render_template("home.html")
    
    

@app.route("/results",methods= ["GET", "POST"])
def results():
    
    query = ""
    toParse=""
    if request.method == 'POST':
        query=request.form['query']
    for url in search (query, stop=3):
        f=urllib.urlopen(url)
        soup = BeautifulSoup(f.read())
        toParse += soup.getText()
    L =findnames(toParse)
    
    return render_template("results.html", L =L[:9])    
    
if __name__=="__main__":
    app.debug=True
    app.run() 
