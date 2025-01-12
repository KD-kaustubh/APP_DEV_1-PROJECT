#App Routes

from flask import Flask,render_template,request
from .models import *
from flask import current_app as app
from datetime import datetime

#many controller and routes here

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        uname=request.form.get('user_name')
        pwd=request.form.get('password')
        usr= User.query.filter_by(username=uname,password=pwd).first()
        if usr and usr.role==0: #existed and admin
            return render_template('admin_dashboard.html')
        if usr and usr.role==1: #existed and user
            return render_template('user_dashboard.html')

    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        uname=request.form.get('user_name')
        pwd=request.form.get('password')
        full_name=request.form.get('full_name')
        qualification=request.form.get('qualification')
        dob=request.form.get('dob')
        dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
        new_usr=User(username=uname,password=pwd,full_name=full_name,qualification=qualification,dob=dob_date)
        db.session.add(new_usr)
        db.session.commit()
        return render_template('login.html')
    
    return render_template('signup.html')

