from flask import Flask,render_template,request
from google import search

# this makes app an instance of the Flask class
# and it passed the special variable __name__ into
# the constructor

app = Flask(__name__)


@app.route("/home", methods= ["GET", "POST"])
@app.route("/",methods= ["GET", "POST"]) 
def home():
    return render_template("home.html")
    
    

@app.route("/results",methods= ["GET", "POST"])
def results():
    L=[]
    query = ""
    if request.method == 'POST':
        query=request.form['query']
    for url in search (query, stop=10):
        L.append(url)
    return render_template("results.html", L =L)    
    
if __name__=="__main__":
    app.debug=True
    app.run() 
