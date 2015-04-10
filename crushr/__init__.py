import sqlite3
from flask import Flask, request, session, g
from contextlib import closing

app = Flask(__name__)

# configuration
app.config.update(dict(
    DATABASE = '/tmp/crushr.db',
    DEBUG = True,
    SECRET_KEY = 'development key',
    DOMAIN = "crushr.com" ))

app.config.from_envvar('APP_SETTINGS', silent=False)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

from crushr import views

if __name__ == '__main__':
    init_db()
    app.run()


