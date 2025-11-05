from flask import Flask, session

def index():
    session['counter'] = 0
    return '<a href="/counter">Дальше</a>'

def counter():
    session['counter'] += 1
    return f"<h1>{session['counter']}</h1>"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KOROLpeCHenek'
app.add_url_rule('/','index',index)
app.add_url_rule('/counter','counter', counter)

if __name__ == '__main__':
    app.run()