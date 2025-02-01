#App Routes

from flask import Flask,render_template,request,redirect,url_for,flash
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
    quizzes=Quiz.query.all()
    return render_template('user_dashboard.html',name=name,quizzes=quizzes)

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

#add quiz routes not completed
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

        new_question = Question(
            quiz_id=quiz_id,
            question_statement=question_statement,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_answer=correct_answer_value)
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
        quiz=Quiz.query.get(quiz_id),option1=request.form.get('option1', ''),option2=request.form.get('option2', ''),option3=request.form.get('option3', ''),option4=request.form.get('option4', '')
    )

# Route to edit a specific question
@app.route('/edit_question/<question_id>/<name>', methods=['GET', 'POST'])
def edit_question(question_id, name):
    question = Question.query.get(question_id)  # Fetch the question by its ID
    if not question:  # If no question is found, handle gracefully
        return redirect(url_for('edit_questions', quiz_id=question.quiz_id, name=name))

    quiz = Quiz.query.get(question.quiz_id)  # Fetch the quiz related to the question
    
    if request.method == 'POST':
        # Update the question fields
        question.question_statement = request.form.get('question_statement')
        question.option1 = request.form.get('option1')
        question.option2 = request.form.get('option2')
        question.option3 = request.form.get('option3')
        question.option4 = request.form.get('option4')
        
        # Set the correct answer based on the selected option
        correct_answer = request.form.get('correct_answer')
        if correct_answer == '1':
            question.correct_answer = question.option1
        elif correct_answer == '2':
            question.correct_answer = question.option2
        elif correct_answer == '3':
            question.correct_answer = question.option3
        elif correct_answer == '4':
            question.correct_answer = question.option4
        
        db.session.commit()  # Save the changes
        
        # After saving, redirect to the page showing all questions for this quiz
        return redirect(url_for('edit_questions', quiz_id=question.quiz_id, name=name))  

    # For GET requests, render the template with the question and quiz
    return render_template('edit_question.html', name=name, question=question, quiz=quiz)

# Route to edit all questions for a specific quiz
@app.route('/edit_questions/<quiz_id>/<name>', methods=['GET'])
def edit_questions(quiz_id, name):
    quiz = Quiz.query.get(quiz_id)  # Fetch the quiz
    questions = Question.query.filter_by(quiz_id=quiz_id).all()  # Fetch all questions for this quiz

    return render_template('edit_questions.html', quiz=quiz, questions=questions, name=name)



#edit quiz
@app.route('/edit_quiz/<id>/<name>', methods=['GET', 'POST'])
def edit_quiz(id, name):
    if request.method == 'POST':
        quiz = Quiz.query.get(id)
        quiz.name = request.form.get('quiz_name')
        quiz.date_of_quiz = request.form.get('date_of_quiz')
        quiz.date_of_quiz = datetime.strptime(quiz.date_of_quiz, '%Y-%m-%d').date()
        quiz.time_duration = request.form.get('time_duration')
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

#submit quiz incommplete
@app.route('/submit_quiz/<id>/<name>', methods=['POST'])
def submit_quiz(id, name):    
    quiz = Quiz.query.get(id)
    user=User.query.filter_by(username=name).first()

    if quiz and user:
        total_score=0
        for question in quiz.questions:
            user_answer = request.form.get(f'question_{question.id}')
            if user_answer==question.correct_answer:
                total_score+=1
        new_score=Score(quiz_id=id,user_id=user.id,time_stamp_of_attempt=datetime.now(),total_score=total_score)
        db.session.add(new_score)
        db.session.commit()

        return redirect(url_for('scores', name=name))

    return redirect(url_for('quiz', name=name))




#SCORES
@app.route('/scores/<name>',methods=['GET','POST'])
def scores(name):
    user=User.query.filter_by(username=name).first()
    if not user:
        return redirect(url_for('home'))
    
    user_scores = (
    db.session.query(Score, Quiz.name)  # Select Score and Quiz name
    .join(Quiz, Score.quiz_id == Quiz.id)  # Join Score with Quiz
    .filter(Score.user_id == user.id)  # Filter only the current user's scores
    .order_by(Score.time_stamp_of_attempt.desc())  # Order by latest attempt
    .all()
)

    return render_template('scores.html',name=name,user_scores=user_scores)





#searching routes incomplete
@app.route('/search/<name>',methods=['GET','POST'])
def search(name):
    if request.method == 'POST':
        search_txt=request.form.get('search_txt')
        by_subject=search_by_subject(search_txt)
        by_chapter=search_by_chapter(search_txt)
        by_quiz=search_by_quiz(search_txt)
        if by_subject:
            return render_template('admin_dashboard.html',name=name,subjects=by_subject)
        elif by_chapter:
            return render_template('admin_dashboard.html',name=name,subjects=by_chapter)
        elif by_quiz:
            return render_template('quiz_dashboard.html',name=name,subjects=by_quiz)
    return redirect(url_for('admin_dashboard',name=name))


#quiz dashboard
@app.route('/quiz/<name>',methods=['GET','POST'])
def quiz(name):
    quizzes=Quiz.query.all()
    return render_template('quiz_dashboard.html',name=name,Quizzes=quizzes)




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

def search_by_quiz(search_txt):
    quizzes=Quiz.query.filter(Quiz.name.ilike(f"%{search_txt}%")).all()
    subjects=[quiz.chapter.subject for quiz in quizzes]
    return subjects