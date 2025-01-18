#App Routes

from flask import Flask,render_template,request,redirect,url_for
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
            return redirect(url_for('admin_dashboard',name=uname)) #render_template('admin_dashboard.html',name=uname)
        elif usr and usr.role==1: #existed and user
            return redirect(url_for('user_dashboard',name=uname)) #render_template('user_dashboard.html',name=uname)
        else:
            return render_template('login.html',err_msg="Invalid User Credentials")#invalid user it will return login page with error message

    return render_template('login.html',err_msg="")

@app.route('/register',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        uname=request.form.get('user_name')
        pwd=request.form.get('password')
        full_name=request.form.get('full_name')
        qualification=request.form.get('qualification')
        dob=request.form.get('dob')
        dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
        usr= User.query.filter_by(username=uname,password=pwd).first()
        if usr:
            return render_template('signup.html',err_msg="User Already Exists")
        new_usr=User(username=uname,password=pwd,full_name=full_name,qualification=qualification,dob=dob_date)
        db.session.add(new_usr)
        db.session.commit()
        return render_template('login.html',err_msg="Registration Successful, Please Login")
    
    return render_template('signup.html',err_msg="")

#common rotes for admin dashboard
@app.route('/admin_dashboard/<name>',methods=['GET','POST'])
def admin_dashboard(name):
    subjects=get_subjects()
    return render_template('admin_dashboard.html',name=name,subjects=subjects)

#common routes for user dashboard
@app.route('/user_dashboard/<name>',methods=['GET','POST'])
def user_dashboard(name):
    return render_template('user_dashboard.html',name=name)

#add_subject routes
@app.route('/add_subjects/<name>',methods=['GET','POST'])
def add_subjects(name):
    if request.method == 'POST':
        sub_name=request.form.get('subject_name')
        sub_description=request.form.get('subject_description')
        new_sub=Subject(name=sub_name,description=sub_description)
        db.session.add(new_sub)
        db.session.commit()
        return redirect(url_for('admin_dashboard',name=name))
    
    return render_template('add_subjects.html',name=name)

#add_chapters routes
@app.route('/add_chapters/<chapter_id>/<name>',methods=['GET','POST'])
def add_chapters(name,chapter_id):
    if request.method == 'POST':
        chapter_name=request.form.get('chapter_name')
        chapter_description=request.form.get('chapter_description')
        new_chapter=Chapter(subject_id=chapter_id,name=chapter_name,description=chapter_description)
        db.session.add(new_chapter)
        db.session.commit()
        return redirect(url_for('admin_dashboard',name=name))
    
    return render_template('add_chapters.html',name=name,chapter_id=chapter_id)

#searching routes
@app.route('/search/<name>',methods=['GET','POST'])
def search(name):
    if request.method == 'POST':
        search_txt=request.form.get('search_txt')
        by_subject=search_by_subject(search_txt)
        by_chapter=search_by_chapter(search_txt)
        if by_subject:
            return render_template('admin_dashboard.html',name=name,subjects=by_subject)
        elif by_chapter:
            return render_template('admin_dashboard.html',name=name,subjects=by_chapter)
    return redirect(url_for('admin_dashboard',name=name))

#edit_subject routes
@app.route('/edit_subject/<id>/<name>', methods=['GET', 'POST'])
def edit_subject(id, name):
    if request.method == 'POST':
        subject = Subject.query.get(id)
        subject.name = request.form.get('subject_name')
        subject.description = request.form.get('subject_description')
        db.session.commit()
        return redirect(url_for('admin_dashboard', name=name))
    return render_template('edit_subject.html', name=name, subject=Subject.query.get(id))

#delete subject
@app.route('/delete_subject/<id>/<name>', methods=['GET', 'POST'])
def delete_subject(id, name):    
    subject = Subject.query.get(id)
    db.session.delete(subject)
    db.session.commit()
    return redirect(url_for('admin_dashboard', name=name))

#delete chapter
@app.route('/delete_chapter/<id>/<name>', methods=['GET', 'POST'])
def delete_chapter(id, name):    
    chapter = Chapter.query.get(id)
    db.session.delete(chapter)
    db.session.commit()
    return redirect(url_for('admin_dashboard', name=name))


#edit chapter routes incomplete
@app.route('/edit_chapter/<id>/<name>', methods=['GET', 'POST'])
def edit_chapter(id, name):
    if request.method == 'POST':
        chapter = Chapter.query.get(id)
        chapter.name = request.form.get('chapter_name')
        chapter.description = request.form.get('chapter_description')
        db.session.commit()
        return redirect(url_for('admin_dashboard', name=name))
    return render_template('edit_chapter.html', name=name, chapter=Chapter.query.get(id))




















#other supported functions
def get_subjects():
    subjects=Subject.query.all()
    return subjects 

def search_by_subject(search_txt):
    subjects=Subject.query.filter(Subject.name.ilike(f"%{search_txt}%")).all()
    return subjects

def search_by_chapter(search_txt):
    chapters=Chapter.query.filter(Chapter.name.ilike(f"%{search_txt}%")).all()
    subjects=[chapter.subject for chapter in chapters]
    return subjects