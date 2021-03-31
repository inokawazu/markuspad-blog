from flask import (Flask, render_template, session, 
                   request, flash, redirect, url_for)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Configurations 
SECRET_KEY = 'sample key'
USERNAME = 'user'
PASSWORD = 'bananacar'
DEBUG = True
SQLALCHEMY_DATABASE_URI= 'sqlite:///posts.db'

# Create App
app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    category = db.relationship('Category',
        backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name

# This is the home-page
@app.route('/')
def index():
   return render_template('index.html')

# This is the research-page
@app.route('/research')
def research_page():
   return render_template('research.html')

# This is the blog-page
@app.route('/blog')
def blog_page():
   return render_template('blog.html')

# This is the about-page
@app.route('/about')
def about_page():
   return render_template('about.html')

#Session(login and logout) - (Inspired by https://github.com/QuadPiece/flask-blog/blob/master/exec.py)
@app.route('/login', methods=['GET', 'POST'])
def login_page():
  error = None
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME']:
      error = 'Invalid username'
    elif request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid password'
    else:
      session['logged_in'] = True
      flash('You were logged in')
      return redirect(url_for('index'))
  return render_template('login.html', error=error)

# this is the main fucntion. 
# Make sure to set debug to False in production.
if __name__ == '__main__':
   app.run(debug=True)
