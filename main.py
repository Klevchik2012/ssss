from flask import (Flask,redirect,url_for,render_template,session,request)
from DB import *
from zapros import *
import os
from random import shuffle

def start_quiz(id = 4):
    start = db.execute(GET_FIRST,(id))
    if len(start) > 0:
        session['last'] = start[0][0]-1
    else:
        session['last'] = 0
    session['quiz'] = id
    session['total'] = 0

def end_quiz():
    session.clear()
    
def question_form(question):
    qid = question[0]
    text = question[1]
    right = question[2]
    unright = question[3].split('$')
    unright.append(right)
    shuffle(unright)
    return render_template('test.html',q_id = qid,text = text, answers = unright)

def save_answers():
    q_id = request.form.get('q_id')
    answer = request.form.get('answer')
    right_ans = db.execute(CHECK,[q_id, answer])
    if not right_ans or len(right_ans) == 0:
        pass
    else:
        session['total'] += 1
    session['last'] = int(q_id)


def index():
    if request.method == 'GET':
        victorina = db.execute(SELECT+'victorina')
        return render_template('index.html',victorina = victorina)
    else:
        qid = request.form.get('victorina')
        start_quiz(qid)
        return redirect(url_for('test'))

def test():
    if request.method == 'POST':
        save_answers()
    resolt = db.execute(NEXT,(session['last'],session['quiz']))
    print(resolt)
    if resolt is None or len(resolt) == 0:   
           return redirect(url_for('result'))

    else:
        return question_form(resolt[0])
    
def result():
    count = db.execute(COUNT_QS,session['quiz'])[0][0]
    total = session['total']
    end_quiz()
    return render_template('result.html', total = total,count = count)



db = DB()
folder = os.getcwd()
app = Flask(__name__,static_folder=folder,template_folder=folder)
app.config['SECRET_KEY'] = 'KOROLpeCHenek'

app.add_url_rule('/','index',index,methods = ['get','post'])
app.add_url_rule('/test','test',test,methods = ['get','post'])
app.add_url_rule('/result','result',result)
app.run()

