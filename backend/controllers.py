#App Routes

from flask import Flask,render_template,request,redirect,url_for,flash,session
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
            return redirect(url_for('admin_dashboard',name=uname)) 
        elif usr and usr.role==1: #existed and user
            return redirect(url_for('user_dashboard',name=uname)) 
        else:
            return render_template('login.html',err_msg="Invalid User Credentials")

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

#common routes for admin dashboard
@app.route('/admin_dashboard/<name>',methods=['GET','POST'])
def admin_dashboard(name):
    subjects=get_subjects()
    return render_template('admin_dashboard.html',name=name,subjects=subjects)

#common routes for user dashboard
@app.route('/user_dashboard/<name>',methods=['GET','POST'])
def user_dashboard(name):
    quizzes=Quiz.query.order_by(Quiz.date_of_quiz.desc()).all()

    today=datetime.now().date()
    
    return render_template('user_dashboard.html',name=name,quizzes=quizzes,today=today)

#---------------------------------------------------------------------------------------------


#CRUD OPERATIONS
#--------------------------------------------------------------------------------------------------

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

#edit chapter routes 
@app.route('/edit_chapter/<id>/<name>', methods=['GET', 'POST'])
def edit_chapter(id, name):
    if request.method == 'POST':
        chapter = Chapter.query.get(id)
        chapter.name = request.form.get('chapter_name')
        chapter.description = request.form.get('chapter_description')
        db.session.commit()
        return redirect(url_for('admin_dashboard', name=name))
    return render_template('edit_chapter.html', name=name, chapter=Chapter.query.get(id))

#add quiz routes
@app.route('/add_quiz/<chapter_id>/<name>',methods=['GET','POST'])
def add_quiz(name,chapter_id):
    if request.method == 'POST':
        quiz_name=request.form.get('quiz_name')
        date=request.form.get('date_of_quiz')
        date_of_quiz=datetime.strptime(date, '%Y-%m-%d').date()

        time_duration=request.form.get('time_duration')
        time_duration = datetime.strptime(time_duration, "%H:%M").time()

        remarks=request.form.get('remarks')
        new_quiz=Quiz(chapter_id=chapter_id,name=quiz_name,date_of_quiz=date_of_quiz,time_duration=time_duration,remarks=remarks)
        db.session.add(new_quiz)
        db.session.commit()

        flash('Quiz added successfully!', 'success')
        return redirect(url_for('admin_dashboard',name=name))
    
    return render_template('add_quiz.html',name=name,chapter_id=chapter_id)



#add question 
@app.route('/add_question/<quiz_id>/<name>', methods=['GET', 'POST'])
def add_question(name, quiz_id):
    if request.method == 'POST':
        question_statement = request.form.get('question_statement')
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')
        option4 = request.form.get('option4')
        correct_answer = request.form.get('correct_answer') 

        if correct_answer == '1':
            correct_answer_value = option1
        elif correct_answer == '2':
            correct_answer_value = option2
        elif correct_answer == '3':
            correct_answer_value = option3
        elif correct_answer == '4':
            correct_answer_value = option4

        new_question = Question(quiz_id=quiz_id,question_statement=question_statement,
        option1=option1,option2=option2,option3=option3,option4=option4,correct_answer=correct_answer_value)
        db.session.add(new_question)
        db.session.commit()

        action = request.form.get('action')
        if action == 'save_next':
            return redirect(url_for('add_question', name=name, quiz_id=quiz_id))
        elif action == 'submit':
            return redirect(url_for('quiz', name=name))

    return render_template(
        'add_question.html',
        name=name,quiz_id=quiz_id,
        quiz=Quiz.query.get(quiz_id),option1=request.form.get('option1', ''),option2=request.form.get('option2', ''),
        option3=request.form.get('option3', ''),option4=request.form.get('option4', ''))


#edit question specific
@app.route('/edit_question/<question_id>/<name>', methods=['GET', 'POST'])
def edit_question(question_id, name):
    question = Question.query.get(question_id)
    if not question: 
        return redirect(url_for('edit_questions', quiz_id=question.quiz_id, name=name))

    quiz = Quiz.query.get(question.quiz_id)  
    
    if request.method == 'POST':
        question.question_statement = request.form.get('question_statement')
        question.option1 = request.form.get('option1')
        question.option2 = request.form.get('option2')
        question.option3 = request.form.get('option3')
        question.option4 = request.form.get('option4')
        
        correct_answer = request.form.get('correct_answer')
        if correct_answer == '1':
            question.correct_answer = question.option1
        elif correct_answer == '2':
            question.correct_answer = question.option2
        elif correct_answer == '3':
            question.correct_answer = question.option3
        elif correct_answer == '4':
            question.correct_answer = question.option4
        
        db.session.commit()
        return redirect(url_for('edit_questions', quiz_id=question.quiz_id, name=name))  

    return render_template('edit_question.html', name=name, question=question, quiz=quiz)

# edit all questions specific quiz
@app.route('/edit_questions/<quiz_id>/<name>', methods=['GET'])
def edit_questions(quiz_id, name):
    quiz = Quiz.query.get(quiz_id)  
    questions = Question.query.filter_by(quiz_id=quiz_id).all()  

    return render_template('edit_questions.html', quiz=quiz, questions=questions, name=name)

#delete specific question
@app.route('/delete_question/<question_id>/<name>', methods=['GET', 'POST'])
def delete_question(question_id, name):
    question = Question.query.get(question_id)
    if question:
        quiz_id = question.quiz_id
        db.session.delete(question)
        db.session.commit()
    return redirect(url_for('edit_questions', quiz_id=quiz_id, name=name))



#QUIZ OPERATIONS
#--------------------------------------------------------------------------------------------------

#edit quiz
@app.route('/edit_quiz/<id>/<name>', methods=['GET', 'POST'])
def edit_quiz(id, name):
    if request.method == 'POST':
        quiz = Quiz.query.get(id)
        quiz.name = request.form.get('quiz_name')
        quiz.date_of_quiz = request.form.get('date_of_quiz')
        quiz.date_of_quiz = datetime.strptime(quiz.date_of_quiz, '%Y-%m-%d').date()
        time_str=request.form.get('time_duration')
        time_obj = datetime.strptime(time_str, "%H:%M").time()
        quiz.time_duration = time_obj
        quiz.remarks = request.form.get('remarks')
        db.session.commit()
        return redirect(url_for('quiz', name=name))
    return render_template('edit_quiz.html', name=name, quiz=Quiz.query.get(id))

#delete quiz
@app.route('/delete_quiz/<id>/<name>', methods=['GET', 'POST'])
def delete_quiz(id, name):    
    quiz = Quiz.query.get(id)
    db.session.delete(quiz)
    db.session.commit()
    return redirect(url_for('quiz', name=name))

#view quiz
@app.route('/view_quiz/<id>/<name>', methods=['GET', 'POST'])
def view_quiz(id, name):    
    quiz = Quiz.query.get(id)
    return render_template('view_quiz.html', name=name,quiz=quiz)

#start quiz
@app.route('/start_quiz/<id>/<name>', methods=['GET', 'POST'])
def start_quiz(id, name):    
    quiz = Quiz.query.get(id)
    return render_template('start_quiz.html', name=name,quiz=quiz)

#submit quiz 
@app.route('/submit_quiz/<id>/<name>', methods=['POST'])
def submit_quiz(id, name):    
    quiz = Question.query.filter_by(quiz_id=id).all()
    user=User.query.filter_by(username=name).first()

    if quiz and user:
        total_score=0
        for question in quiz:
            user_answer = request.form.get(f'question_{question.id}')
            if user_answer==question.correct_answer:
                total_score+=1
        new_score=Score(quiz_id=id,user_id=user.id,time_stamp_of_attempt=datetime.now(),total_score=total_score)
        db.session.add(new_score)
        db.session.commit()

        return redirect(url_for('scores', name=name))

    return redirect(url_for('quiz', name=name))


#SCORES user specific
@app.route('/scores/<name>',methods=['GET','POST'])
def scores(name):
    user=User.query.filter_by(username=name).first()
    if not user:
        return redirect(url_for('home'))
    
    user_scores = (
    db.session.query(Score, Quiz.name).join(Quiz, Score.quiz_id == Quiz.id)  .filter(Score.user_id == user.id) .order_by(Score.time_stamp_of_attempt.desc()).all())

    return render_template('scores.html',name=name,user_scores=user_scores)


#admin specific user summary routes

@app.route('/admin/user_summary/<int:user_id>', methods=['GET'])
def user_summary(user_id):
    user = User.query.get_or_404(user_id)

    # Fetch quiz attempts of the user
    quiz_attempts = db.session.query(Score.time_stamp_of_attempt, Subject.name.label('subject')) \
        .join(Quiz, Score.quiz_id == Quiz.id) \
        .join(Chapter, Quiz.chapter_id == Chapter.id) \
        .join(Subject, Chapter.subject_id == Subject.id) \
        .filter(Score.user_id == user_id) \
        .all()

    month_counts = {}
    subject_counts = {}

    for time_stamp, subject in quiz_attempts:
        month = time_stamp.strftime('%B')  # Extract month
        month_counts[month] = month_counts.get(month, 0) + 1
        subject_counts[subject] = subject_counts.get(subject, 0) + 1

    # Monthly bar chart
    fig_month_bar = plt.figure(figsize=(6, 4))
    plt.bar(month_counts.keys(), month_counts.values(), color='skyblue')
    plt.xlabel('Month')
    plt.ylabel('Total Quiz Attempts')
    plt.title('Quiz Attempts (Monthly)')
    img_month_bar = io.BytesIO()
    FigureCanvas(fig_month_bar).print_png(img_month_bar)
    img_month_bar.seek(0)
    month_bar_chart_url = base64.b64encode(img_month_bar.getvalue()).decode('utf8')

    # Subject pie chart
    fig_subject_pie = plt.figure(figsize=(6, 4))
    plt.pie(subject_counts.values(), labels=subject_counts.keys(), autopct='%1.1f%%', startangle=90)
    plt.title('Quiz Attempts by Subject')
    img_subject_pie = io.BytesIO()
    FigureCanvas(fig_subject_pie).print_png(img_subject_pie)
    img_subject_pie.seek(0)
    subject_pie_chart_url = base64.b64encode(img_subject_pie.getvalue()).decode('utf8')


    return render_template(
        'admin_user_summary.html',
        name=user.full_name,month_bar_chart_url=month_bar_chart_url,subject_pie_chart_url=subject_pie_chart_url,subject_counts=subject_counts,month_counts=month_counts)


#-------------------------------------------------------------------------------------------
#user summary charts
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import io
import base64
from flask import render_template, redirect, url_for
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

@app.route('/summary/<name>', methods=['GET'])
def summary(name):
    user = User.query.filter_by(username=name).first()
    if not user:
        return redirect(url_for('home'))
    
    #all quizzes by user with subject from chapter
    user_scores = (
        db.session.query(Score, Quiz.name, Subject.name.label('subject'), Score.time_stamp_of_attempt)
        .join(Quiz, Score.quiz_id == Quiz.id)
        .join(Chapter, Quiz.chapter_id == Chapter.id)  
        .join(Subject, Chapter.subject_id == Subject.id) 
        .filter(Score.user_id == user.id)
        .all())

    subject_counts = {}
    month_counts = {}

    for score, quiz_name, subject, time_stamp in user_scores:
        month = time_stamp.strftime('%B')

        #count subject quizzes
        subject_counts[subject] = subject_counts.get(subject, 0) + 1

        #count quizzes
        month_counts[month] = month_counts.get(month, 0) + 1

    #subject wise pie chart
    fig_subject_pie = plt.figure(figsize=(6, 4))
    plt.pie(subject_counts.values(), labels=subject_counts.keys(), autopct='%1.1f%%', startangle=90)
    plt.title('Subject-wise Quiz Attempts')

    img_subject_pie = io.BytesIO()
    FigureCanvas(fig_subject_pie).print_png(img_subject_pie)
    img_subject_pie.seek(0)
    subject_pie_chart_url = base64.b64encode(img_subject_pie.getvalue()).decode('utf8')

    # Generate Month-wise Bar Chart
    fig_month_bar = plt.figure(figsize=(6, 4))
    plt.bar(month_counts.keys(), month_counts.values(), color='skyblue')
    plt.xlabel('Month')
    plt.ylabel('Attempt Count')
    plt.title('Month-wise Quiz Attempts')

    img_month_bar = io.BytesIO()
    FigureCanvas(fig_month_bar).print_png(img_month_bar)
    img_month_bar.seek(0)
    month_bar_chart_url = base64.b64encode(img_month_bar.getvalue()).decode('utf8')

    return render_template(
        'user_summary.html',name=name,subject_counts=subject_counts,month_counts=month_counts,
        subject_pie_chart_url=subject_pie_chart_url,month_bar_chart_url=month_bar_chart_url)


@app.route('/admin/summary', methods=['GET'])
def admin_summary():
    # Permanent admin
    name = session.get("username", "Admin")  
    # Total user counts
    total_users = User.query.count()
    total_admins = User.query.filter_by(role=0).count()
    total_students = total_users - total_admins
    # Total quizzes
    total_quizzes = Quiz.query.count()

    # Quiz attempts data
    quiz_attempts = db.session.query(Score.time_stamp_of_attempt, Subject.name.label('subject')) \
        .join(Quiz, Score.quiz_id == Quiz.id) \
        .join(Chapter, Quiz.chapter_id == Chapter.id) \
        .join(Subject, Chapter.subject_id == Subject.id) \
        .all()

    month_counts = {}
    subject_counts = {}

    for time_stamp, subject in quiz_attempts:
        month = time_stamp.strftime('%B')  # Extract month
        month_counts[month] = month_counts.get(month, 0) + 1
        subject_counts[subject] = subject_counts.get(subject, 0) + 1

    # Monthly bar chart
    fig_month_bar = plt.figure(figsize=(6, 4))
    plt.bar(month_counts.keys(), month_counts.values(), color='skyblue')
    plt.xlabel('Month')
    plt.ylabel('Total Quiz Attempts')
    plt.title('Overall Quiz Attempts (Monthly)')
    img_month_bar = io.BytesIO()
    FigureCanvas(fig_month_bar).print_png(img_month_bar)
    img_month_bar.seek(0)
    month_bar_chart_url = base64.b64encode(img_month_bar.getvalue()).decode('utf8')

    # Subject pie chart
    fig_subject_pie = plt.figure(figsize=(6, 4))
    plt.pie(subject_counts.values(), labels=subject_counts.keys(), autopct='%1.1f%%', startangle=90)
    plt.title('Overall Quiz Attempts by Subject')
    img_subject_pie = io.BytesIO()
    FigureCanvas(fig_subject_pie).print_png(img_subject_pie)
    img_subject_pie.seek(0)
    subject_pie_chart_url = base64.b64encode(img_subject_pie.getvalue()).decode('utf8')

    # Top 5 user avg score per attempt
    top_users = db.session.query(
        User.full_name, 
        (db.func.sum(Score.total_score) / db.func.count(Score.id)).label("avg_score")).join(Score, User.id == Score.user_id).group_by(User.id) .order_by(db.desc("avg_score")) .limit(5) .all()

    # Get the list of all users
    users_list = User.query.filter(User.role == 1).all()

    return render_template(
        'admin_summary.html',
        name=name,
        total_users=total_users,total_admins=total_admins,total_students=total_students,total_quizzes=total_quizzes,
        month_bar_chart_url=month_bar_chart_url,
        subject_pie_chart_url=subject_pie_chart_url,top_users=top_users,users_list=users_list  
    )



#------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------




#searching routes
#admin search
@app.route('/adminsearch/<name>',methods=['GET','POST'])
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

#user search
@app.route('/usersearch/<name>', methods=['GET', 'POST'])
def user_search(name):
    if request.method == 'POST':
        search_txt = request.form.get('search_txt')
        
        if search_txt:
            # Search in quizzes by subject or quiz name
            quizzes = search_quiz_by_subject_or_quiz(search_txt)
            # Search in quizzes by subject or chapter name
            chapters = search_quiz_by_subject_or_chapter(search_txt)
            
            today = datetime.now().date()
            return render_template('user_dashboard.html', name=name, quizzes=quizzes, chapters=chapters, today=today)
    
    return redirect(url_for('user_dashboard', name=name))


        





#admin quiz dashboard
@app.route('/quiz/<name>',methods=['GET','POST'])
def quiz(name):
    quizzes=Quiz.query.all()
    return render_template('admin_quizdashboard.html',name=name,Quizzes=quizzes)

#score dashboard
@app.route('/score_dashboard/<name>',methods=['GET','POST'])
def score_dashboard(name):
    scores=Score.query.all()
    return render_template('scores.html',name=name,scores=scores)


#-------------------------------------------------------------------------------------------
#other supported functions
def get_subjects():
    subjects=Subject.query.all()
    return subjects 

def get_quiz():
    quizzes=Quiz.query.all()
    return quizzes

def search_by_subject(search_txt):
    subjects=Subject.query.filter(Subject.name.ilike(f"%{search_txt}%")).all()
    return subjects

def search_by_chapter(search_txt):
    chapters=Chapter.query.filter(Chapter.name.ilike(f"%{search_txt}%")).all()
    subjects=[chapter.subject for chapter in chapters]
    return subjects

#user search routes
def search_quiz_by_subject_or_quiz(search_term):
    if search_term:
        #Search quizzes based on subject name or quiz name
        return Quiz.query.join(Chapter).join(Subject).filter((Subject.name.ilike(f'%{search_term}%')) | (Quiz.name.ilike(f'%{search_term}%'))).all()
    return []


def search_quiz_by_subject_or_chapter(search_term):
    if search_term:
        #Search chapters based on the subject name or chapter name
        return Chapter.query.join(Subject).filter((Subject.name.ilike(f'%{search_term}%')) | (Chapter.name.ilike(f'%{search_term}%'))).all()
    return []


