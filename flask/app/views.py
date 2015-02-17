from app import app
from flask import render_template

@app.route('/')
@app.route('/<tag>')
def index(tag=None):
    return render_template('index.html', tag=tag)
