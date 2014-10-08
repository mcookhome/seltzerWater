from flask import Flask,render_template,request


# this makes app an instance of the Flask class
# and it passed the special variable __name__ into
# the constructor

app = Flask(__name__)


@app.route("/home", methods= ["GET", "POST"])
@app.route("/",methods= ["GET", "POST"]) 
def home():
    if request.method== "GET":
        pass
        
    else:
        team=request.form["bar"]
        print team
    return render_template("home.html")
if __name__=="__main__":
    app.debug=True
    app.run() 
