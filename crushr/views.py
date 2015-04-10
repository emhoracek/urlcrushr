from crushr import app
from flask import render_template, g, redirect, request
from random import choice

def make_intense_word (length):
    word = ""
    intense_letters =['A', 'O', 'W', 'G', 'K', 'P', 'R', 'T', 'U']
    for n in range(length):
        word = word + choice (intense_letters)
    return word

def crushit (longer):
    shorter = None
    while shorter is None:
        try:
            shorter = make_intense_word(5) 
            insert_db(shorter, longer)
        except:
            pass
    return shorter

def query_db ( query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0][0] if rv else None) if one else rv

def query_longer(url):
    sql = "SELECT long_url FROM urls WHERE short_url = ?"
    return query_db(sql, (url,), one=True)

def query_shorter(url):
    sql = "SELECT short_url FROM urls WHERE long_url = ?"
    return query_db(sql, (url,), one=True)

def insert_db(shorter, longer):
    print("Inserting the long url was " + longer + 
            " and shorter url was " + shorter)
    sql = "INSERT INTO urls (short_url, long_url) values (?, ?)"
    g.db.execute(sql, (shorter, longer))
    g.db.commit()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/add', methods=["POST"])
def add():
    longer = request.form['url']
    shorter = crushit(longer)
    print("The long url was " + longer + 
            " and shorter url was " + shorter)
    return render_template("add.html",
                           domain = app.config.DOMAIN,
                           longer = longer,
                           shorter = shorter)

@app.route('/<shorter>')
def short_url(shorter=None):
    longer = query_longer(shorter)
    print(shorter)
    return redirect(longer) 
