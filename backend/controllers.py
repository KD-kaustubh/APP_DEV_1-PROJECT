#App Routes - SECURE VERSION with Flask-Login, Bcrypt, and CSRF Protection

from flask import Flask, render_template, request, redirect, url_for, flash, session
from .models import *
from .forms import LoginForm, SignupForm, SubjectForm, ChapterForm, QuizForm, QuestionForm
from flask import current_app as app
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from functools import wraps
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import io
import base64
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

#many controller and routes here

def admin_required(f):
    """Decorator to check if user is admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 0:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard') if current_user.role == 0 else url_for('user_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data) and user.is_active:
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else (
                redirect(url_for('admin_dashboard')) if user.role == 0 else redirect(url_for('user_dashboard'))
            )
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = SignupForm()
    if form.validate_on_submit():
        try:
            dob_date = datetime.strptime(form.dob.data.isoformat(), '%Y-%m-%d').date()
            
            new_user = User(
                username=form.username.data,
                full_name=form.full_name.data,
                qualification=form.qualification.data,
                dob=dob_date,
                role=1  # Default role is User
            )
            new_user.set_password(form.password.data)  # Hash password
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('signin'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'danger')
    
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    # Clear any existing flash messages before logging out
    session.pop('_flashes', None)
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('home'))

#common routes for admin dashboard
@app.route('/admin_dashboard', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_dashboard():
    subjects = get_subjects()
    return render_template('admin_dashboard.html', name=current_user.username, subjects=subjects)

#common routes for user dashboard
@app.route('/user_dashboard', methods=['GET', 'POST'])
@login_required
def user_dashboard():
    if current_user.role == 0:  # If admin, redirect to admin dashboard
        return redirect(url_for('admin_dashboard'))
    
    quizzes = Quiz.query.order_by(Quiz.date_of_quiz.desc()).all()
    today = datetime.now().date()
    
    return render_template('user_dashboard.html', name=current_user.username, quizzes=quizzes, today=today)

#---------------------------------------------------------------------------------------------


#CRUD OPERATIONS
#--------------------------------------------------------------------------------------------------

#add_subject routes
@app.route('/add_subjects', methods=['GET', 'POST'])
@login_required
@admin_required
def add_subjects():
    form = SubjectForm()
    if form.validate_on_submit():
        try:
            new_sub = Subject(name=form.name.data, description=form.description.data)
            db.session.add(new_sub)
            db.session.commit()
            flash('Subject added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to add subject: {str(e)}', 'danger')
    
    return render_template('add_subjects.html', form=form, name=current_user.username)

#add_chapters routes
@app.route('/add_chapters/<int:chapter_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def add_chapters(chapter_id):
    form = ChapterForm()
    if form.validate_on_submit():
        try:
            new_chapter = Chapter(
                subject_id=chapter_id,
                name=form.name.data,
                description=form.description.data
            )
            db.session.add(new_chapter)
            db.session.commit()
            flash('Chapter added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to add chapter: {str(e)}', 'danger')
    
    return render_template('add_chapters.html', form=form, name=current_user.username, chapter_id=chapter_id)

#edit_subject routes
@app.route('/edit_subject/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_subject(id):
    subject = Subject.query.get_or_404(id)
    form = SubjectForm()
    
    if form.validate_on_submit():
        try:
            subject.name = form.name.data
            subject.description = form.description.data
            db.session.commit()
            flash('Subject updated successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to update subject: {str(e)}', 'danger')
    elif request.method == 'GET':
        form.name.data = subject.name
        form.description.data = subject.description
    
    return render_template('edit_subject.html', name=current_user.username, subject=subject, form=form)

#delete subject
@app.route('/delete_subject/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_subject(id):    
    subject = Subject.query.get_or_404(id)
    try:
        db.session.delete(subject)
        db.session.commit()
        flash('Subject deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to delete subject: {str(e)}', 'danger')
    
    return redirect(url_for('admin_dashboard'))

#delete chapter
@app.route('/delete_chapter/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_chapter(id):    
    chapter = Chapter.query.get_or_404(id)
    try:
        db.session.delete(chapter)
        db.session.commit()
        flash('Chapter deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to delete chapter: {str(e)}', 'danger')
    
    return redirect(url_for('admin_dashboard'))

#edit chapter routes 
@app.route('/edit_chapter/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_chapter(id):
    chapter = Chapter.query.get_or_404(id)
    form = ChapterForm()
    
    if form.validate_on_submit():
        try:
            chapter.name = form.name.data
            chapter.description = form.description.data
            db.session.commit()
            flash('Chapter updated successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to update chapter: {str(e)}', 'danger')
    elif request.method == 'GET':
        form.name.data = chapter.name
        form.description.data = chapter.description
    
    return render_template('edit_chapter.html', name=current_user.username, chapter=chapter, form=form)

#add quiz routes
@app.route('/add_quiz/<int:chapter_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def add_quiz(chapter_id):
    form = QuizForm()
    if form.validate_on_submit():
        try:
            date_of_quiz = datetime.strptime(form.date_of_quiz.data.isoformat(), '%Y-%m-%d').date()
            time_duration = datetime.strptime(form.time_duration.data, "%H:%M").time()
            
            new_quiz = Quiz(
                chapter_id=chapter_id,
                name=form.name.data,
                date_of_quiz=date_of_quiz,
                time_duration=time_duration,
                remarks=form.remarks.data
            )
            db.session.add(new_quiz)
            db.session.commit()
            flash('Quiz added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to add quiz: {str(e)}', 'danger')
    
    return render_template('add_quiz.html', form=form, name=current_user.username, chapter_id=chapter_id)



#add question 
@app.route('/add_question/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def add_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuestionForm()
    
    if form.validate_on_submit():
        try:
            # Get correct answer based on selection
            correct_answer_map = {
                '1': form.option1.data,
                '2': form.option2.data,
                '3': form.option3.data,
                '4': form.option4.data
            }
            correct_answer = correct_answer_map.get(form.correct_answer.data)
            
            new_question = Question(
                quiz_id=quiz_id,
                question_statement=form.question_statement.data,
                option1=form.option1.data,
                option2=form.option2.data,
                option3=form.option3.data,
                option4=form.option4.data,
                correct_answer=correct_answer
            )
            db.session.add(new_question)
            db.session.commit()
            
            flash('Question added successfully!', 'success')
            
            # Determine action
            if request.form.get('action') == 'save_next':
                return redirect(url_for('add_question', quiz_id=quiz_id))
            else:
                return redirect(url_for('quiz'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to add question: {str(e)}', 'danger')
    
    return render_template(
        'add_question.html',
        form=form,
        name=current_user.username,
        quiz_id=quiz_id,
        quiz=quiz
    )


#edit question specific
@app.route('/edit_question/<int:question_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_question(question_id):
    question = Question.query.get_or_404(question_id)
    quiz = Quiz.query.get_or_404(question.quiz_id)
    form = QuestionForm()
    
    if form.validate_on_submit():
        try:
            question.question_statement = form.question_statement.data
            question.option1 = form.option1.data
            question.option2 = form.option2.data
            question.option3 = form.option3.data
            question.option4 = form.option4.data
            
            correct_answer_map = {
                '1': form.option1.data,
                '2': form.option2.data,
                '3': form.option3.data,
                '4': form.option4.data
            }
            question.correct_answer = correct_answer_map.get(form.correct_answer.data)
            
            db.session.commit()
            flash('Question updated successfully!', 'success')
            return redirect(url_for('edit_questions', quiz_id=question.quiz_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to update question: {str(e)}', 'danger')
    elif request.method == 'GET':
        form.question_statement.data = question.question_statement
        form.option1.data = question.option1
        form.option2.data = question.option2
        form.option3.data = question.option3
        form.option4.data = question.option4
    
    return render_template('edit_question.html', name=current_user.username, question=question, quiz=quiz, form=form)

# edit all questions specific quiz
@app.route('/edit_questions/<int:quiz_id>', methods=['GET'])
@login_required
@admin_required
def edit_questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)  
    questions = Question.query.filter_by(quiz_id=quiz_id).all()  

    return render_template('edit_questions.html', quiz=quiz, questions=questions, name=current_user.username)

#delete specific question
@app.route('/delete_question/<int:question_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    quiz_id = question.quiz_id
    try:
        db.session.delete(question)
        db.session.commit()
        flash('Question deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to delete question: {str(e)}', 'danger')
    
    return redirect(url_for('edit_questions', quiz_id=quiz_id))



#QUIZ OPERATIONS
#--------------------------------------------------------------------------------------------------

#edit quiz
@app.route('/edit_quiz/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    form = QuizForm()
    
    if form.validate_on_submit():
        try:
            quiz.name = form.name.data
            quiz.date_of_quiz = datetime.strptime(form.date_of_quiz.data.isoformat(), '%Y-%m-%d').date()
            quiz.time_duration = datetime.strptime(form.time_duration.data, "%H:%M").time()
            quiz.remarks = form.remarks.data
            db.session.commit()
            flash('Quiz updated successfully!', 'success')
            return redirect(url_for('quiz'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to update quiz: {str(e)}', 'danger')
    elif request.method == 'GET':
        form.name.data = quiz.name
        form.date_of_quiz.data = quiz.date_of_quiz
        form.remarks.data = quiz.remarks
    
    return render_template('edit_quiz.html', name=current_user.username, quiz=quiz, form=form)

#delete quiz
@app.route('/delete_quiz/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_quiz(id):    
    quiz = Quiz.query.get_or_404(id)
    try:
        db.session.delete(quiz)
        db.session.commit()
        flash('Quiz deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to delete quiz: {str(e)}', 'danger')
    
    return redirect(url_for('quiz'))

#view quiz
@app.route('/view_quiz/<int:id>', methods=['GET', 'POST'])
@login_required
def view_quiz(id):    
    quiz = Quiz.query.get_or_404(id)
    return render_template('view_quiz.html', name=current_user.username, quiz=quiz)

#start quiz
@app.route('/start_quiz/<int:id>', methods=['GET', 'POST'])
@login_required
def start_quiz(id):    
    quiz = Quiz.query.get_or_404(id)
    return render_template('start_quiz.html', name=current_user.username, quiz=quiz)

#submit quiz 
@app.route('/submit_quiz/<int:id>', methods=['POST'])
@login_required
def submit_quiz(id):    
    quiz_questions = Question.query.filter_by(quiz_id=id).all()
    
    if quiz_questions and current_user:
        total_score = 0
        for question in quiz_questions:
            user_answer = request.form.get(f'question_{question.id}')
            # Debug: Print comparison
            print(f"Question {question.id}:")
            print(f"  User answer: '{user_answer}' (type: {type(user_answer)})")
            print(f"  Correct answer: '{question.correct_answer}' (type: {type(question.correct_answer)})")
            print(f"  Match: {user_answer == question.correct_answer}")
            
            if user_answer and user_answer.strip() == question.correct_answer.strip():
                total_score += 1
                print(f"  ✓ Correct!")
            else:
                print(f"  ✗ Wrong")
        
        print(f"Total score: {total_score} out of {len(quiz_questions)}")
        
        try:
            new_score = Score(
                quiz_id=id,
                user_id=current_user.id,
                time_stamp_of_attempt=datetime.now(),
                total_score=total_score
            )
            db.session.add(new_score)
            db.session.commit()
            flash('Quiz submitted successfully!', 'success')
            return redirect(url_for('scores'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to submit quiz: {str(e)}', 'danger')

    return redirect(url_for('user_dashboard'))


#SCORES user specific
@app.route('/scores', methods=['GET', 'POST'])
@login_required
def scores():
    if current_user.role == 0:  # If admin, redirect to admin summary
        return redirect(url_for('admin_summary'))
    
    user_scores = (
        db.session.query(Score, Quiz.name)
        .join(Quiz, Score.quiz_id == Quiz.id)
        .filter(Score.user_id == current_user.id)
        .order_by(Score.time_stamp_of_attempt.desc())
        .all()
    )

    return render_template('scores.html', name=current_user.username, user_scores=user_scores)


#admin specific user summary routes

@app.route('/admin/user_summary/<int:user_id>', methods=['GET'])
@login_required
@admin_required
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
@app.route('/summary', methods=['GET'])
@login_required
def summary():
    if current_user.role == 0:  # If admin, redirect to admin summary
        return redirect(url_for('admin_summary'))
    
    #all quizzes by user with subject from chapter
    user_scores = (
        db.session.query(Score, Quiz.name, Subject.name.label('subject'), Score.time_stamp_of_attempt)
        .join(Quiz, Score.quiz_id == Quiz.id)
        .join(Chapter, Quiz.chapter_id == Chapter.id)  
        .join(Subject, Chapter.subject_id == Subject.id) 
        .filter(Score.user_id == current_user.id)
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
        'user_summary.html',name=current_user.username,subject_counts=subject_counts,month_counts=month_counts,
        subject_pie_chart_url=subject_pie_chart_url,month_bar_chart_url=month_bar_chart_url)


@app.route('/admin/summary', methods=['GET'])
@login_required
@admin_required
def admin_summary():
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
        name=current_user.username,
        total_users=total_users,total_admins=total_admins,total_students=total_students,total_quizzes=total_quizzes,
        month_bar_chart_url=month_bar_chart_url,
        subject_pie_chart_url=subject_pie_chart_url,top_users=top_users,users_list=users_list  
    )



#------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------




#searching routes
#admin search
@app.route('/adminsearch', methods=['GET', 'POST'])
@login_required
@admin_required
def search():
    if request.method == 'POST':
        search_txt = request.form.get('search_txt', '').strip()
        by_subject = search_by_subject(search_txt)
        by_chapter = search_by_chapter(search_txt)
        if by_subject:
            return render_template('admin_dashboard.html', name=current_user.username, subjects=by_subject)
        elif by_chapter:
            return render_template('admin_dashboard.html', name=current_user.username, subjects=by_chapter)
    return redirect(url_for('admin_dashboard'))

#user search
@app.route('/usersearch', methods=['GET', 'POST'])
@login_required
def user_search():
    if request.method == 'POST':
        search_txt = request.form.get('search_txt', '').strip()
        
        if search_txt:
            # Search in quizzes by subject or quiz name
            quizzes = search_quiz_by_subject_or_quiz(search_txt)
            # Search in quizzes by subject or chapter name
            chapters = search_quiz_by_subject_or_chapter(search_txt)
            
            today = datetime.now().date()
            return render_template('user_dashboard.html', name=current_user.username, quizzes=quizzes, chapters=chapters, today=today)
    
    return redirect(url_for('user_dashboard'))


        





#admin quiz dashboard
@app.route('/quiz', methods=['GET', 'POST'])
@login_required
@admin_required
def quiz():
    quizzes = Quiz.query.all()
    return render_template('admin_quizdashboard.html', name=current_user.username, Quizzes=quizzes)

#score dashboard
@app.route('/score_dashboard', methods=['GET', 'POST'])
@login_required
@admin_required
def score_dashboard():
    scores = Score.query.all()
    return render_template('scores.html', name=current_user.username, scores=scores)


#-------------------------------------------------------------------------------------------
#other supported functions
def get_subjects():
    subjects = Subject.query.all()
    return subjects 

def get_quiz():
    quizzes = Quiz.query.all()
    return quizzes

def search_by_subject(search_txt):
    subjects = Subject.query.filter(Subject.name.ilike(f"%{search_txt}%")).all()
    return subjects

def search_by_chapter(search_txt):
    chapters = Chapter.query.filter(Chapter.name.ilike(f"%{search_txt}%")).all()
    subjects = [chapter.subject for chapter in chapters]
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


