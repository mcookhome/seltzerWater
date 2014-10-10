from flask import Flask,render_template,request
from google import search
import urllib,pickle,re
from bs4 import BeautifulSoup
from collections import Counter
import operator,unicodedata
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

def finddates(g):
    #r = re.compile('^((((0[13578])|([13578])|(1[02]))[\/](([1-9])|([0-2][0-9])|(3[01])))|(((0[469])|([469])|(11))[\/](([1-9])|([0-2][0-9])|(30)))|((2|02)[\/](([1-9])|([0-2][0-9]))))[\/]\d{4}$|^\d{4}$')
    r = re.compile('(?:[A-Z][a-z].\.)* (?:[A-Z][a-z]+)(?:\s[A-Z][a-z]+)+')
    M=r.findall(g)
    y=0
    print M
    for i in xrange(len(M)):
        M[i] = M[i].replace('\n','')
    return M 



@app.route("/home", methods= ["GET", "POST"])
@app.route("/",methods= ["GET", "POST"]) 
def home():
    return render_template("home.html")
    
    

@app.route("/who",methods= ["GET", "POST"])
def who():
    
    query = ""
    toParse=""
    if request.method == 'POST':
        query=request.form['query']
    i=0
    for url in search(query, stop=5):
        print "hello is this alive"
        f=urllib.urlopen(url)
        soup = BeautifulSoup(f.read())
        f.close()
        toParse += soup.getText()
        i=i+1
        if i>4:
            break
    print "im out"
    toParse = unicodedata.normalize('NFKD',toParse).encode('ascii','ignore')
    L =findnames(toParse)
    s=""
    for x in xrange(len(L)):
        for y in L[x]:
            s+= y + " "
        L[x] = s[1:-1]
        s=""
        
    #testing
    c= Counter(L)
    answer = c.most_common(20)
    common = []
    for x in answer:
        string, count = x
        #print string
        common.append(string)
        #print common
    #testing
    return render_template("who.html", L =L,common=common)  

@app.route("/when",methods= ["GET", "POST"])
def when():
    
    query = ""
    toParse=""
    if request.method == 'POST':
        query=request.form['query']
    i=0
    for url in search(query, stop=5):
        print "hello is this alive"
        f=urllib.urlopen(url)
        soup = BeautifulSoup(f.read())
        f.close()
        toParse += soup.getText()
        i=i+1
        if i>4:
            break
    print "im out"

    toParse = unicodedata.normalize('NFKD',toParse).encode('ascii','ignore')
    M =finddates(toParse)
    print M
    s=""
    for x in xrange(len(M)):
        for y in M[x]:
            s+= y + " "
        M[x] = s[1:-1]
        s=""
        
    #testing
    c= Counter(M)
    answer = c.most_common(20)
    common = []
    for x in answer:
        string, count = x
        #print string
        common.append(string)
        #print common
    #testing
    return render_template("when.html", M =M,common=common)    
    
if __name__=="__main__":
    app.debug=True
    app.run() 
