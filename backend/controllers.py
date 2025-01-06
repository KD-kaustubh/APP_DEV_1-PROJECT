#App Routes

from flask import Flask,render_template
from flask import current_app as app

#many controller and roters here

@app.route('/')
def home():
    return render_template('index.html')