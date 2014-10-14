from flask import Flask,render_template,request
from google import search
import urllib2,pickle,re, time, threading,unicodedata
from bs4 import BeautifulSoup
from collections import Counter
# this makes app an instance of the Flask class
# and it passed the special variable __name__ into
# the constructor

app = Flask(__name__)

h = open('diction.txt','rb')
d= pickle.load(h)
h.close()
 
#used to work with timeout issues on beautifulsoup

class Ticker(threading.Thread):
  """A very simple thread that merely blocks for :attr:`interval` and sets a
  :class:`threading.Event` when the :attr:`interval` has elapsed. It then waits
  for the caller to unset this event before looping again.

  Example use::

    t = Ticker(1.0) # make a ticker
    t.start() # start the ticker in a new thread
    try:
      while t.evt.wait(): # hang out til the time has elapsed
        t.evt.clear() # tell the ticker to loop again
        print time.time(), "FIRING!"
    except:
      t.stop() # tell the thread to stop
      t.join() # wait til the thread actually dies

  """
  # SIGALRM based timing proved to be unreliable on various python installs,
  # so we use a simple thread that blocks on sleep and sets a threading.Event
  # when the timer expires, it does this forever.
  def __init__(self, interval):
    super(Ticker, self).__init__()
    self.interval = interval
    self.evt = threading.Event()
    self.evt.clear()
    self.should_run = threading.Event()
    self.should_run.set()

  def stop(self):
    """Stop the this thread. You probably want to call :meth:`join` immediately
    afterwards
    """
    self.should_run.clear()

  def consume(self):
    was_set = self.evt.is_set()
    if was_set:
      self.evt.clear()
    return was_set

  def run(self):
    """The internal main method of this thread. Block for :attr:`interval`
    seconds before setting :attr:`Ticker.evt`

    .. warning::
      Do not call this directly!  Instead call :meth:`start`.
    """
    while self.should_run.is_set():
      time.sleep(self.interval)
      self.evt.set()
#end working with timeouts
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
    #r = re.compile('(?:^(?:19|20)\d\d[- /.](?:0[1-9]|1[012])[- /.](?:0[1-9]|[12][0-9]|3[01])$)|(?:^(?:0[1-9]|1[012])[- /.](?:0[1-9]|[12][0-9]|3[01])(?:(?:19|20)\d\d[- /.])$)')
    r = re.compile('[A-Z][a-z]+[\.]*\s[123]*[0-9],*\s\s*[1-9][0-9]+')
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
        f=urllib2.urlopen(url)

        t = Ticker(2)
        t.start()
        try: 
            while t.evt.wait():
                lines = f.read()
                print "f"
                soup = BeautifulSoup(lines )
                f.close()
                toParse += soup.getText()
                i=i+1
                t.stop()
                t.join()
        except:
            t.stop()
            t.join()
            print "too long :("
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
    c= Counter(L)
    answer = c.most_common(20)
    common = []
    for x in answer:
        string, count = x
        #print string
        common.append(string)
        #print common
    while common[0] in query:
      common.remove(common[0])
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
        f=urllib2.urlopen(url)
        t = Ticker(2)
        t.start()
        try: 
          while t.evt.wait():
            lines = f.read()
            print "f"
            soup = BeautifulSoup(lines )
            f.close()
            toParse += soup.getText()
            i=i+1
            t.stop()
            t.join()
        except:
          t.stop()
          t.join()
          print "too long :("
        if i>4:
          break
    print "im out"
    toParse = unicodedata.normalize('NFKD',toParse).encode('ascii','ignore')
    L =finddates(toParse)
    print L
    s=""
    for x in xrange(len(L)):
        for y in L[x]:
            s+= y + " "
        s=""
      
  
    c= Counter(L)
    answer = c.most_common(20)
    common = []
    for x in answer:
        string, count = x
        #print string
        common.append(string)
        #print common
    while common[0] in query:
      common.remove(common[0])
      

    return render_template("when.html", L=L,common=common)    
    
if __name__=="__main__":
    app.debug=True
    app.run() 
