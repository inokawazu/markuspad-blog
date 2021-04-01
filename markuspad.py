from flask import (Flask, render_template, session, 
                   request, flash, redirect, url_for)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Configurations 
SECRET_KEY = 'sample key'
USERNAME = 'user'
PASSWORD = 'pass'
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///posts.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True

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

# Make and edit Posts
@app.route('/make/')
def make_post_page():
    pass

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Session(login and logout) - (Inspired by https://github.com/QuadPiece/flask-blog/blob/master/exec.py)

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403

#Decorator to require login to views.
def require_login(func):
    def func_with_login(*args, **kwargs):
        if not session['logged_in']:
            return render_template('403.html')
        return func(*args, **kwargs)

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

@app.route('/logout')
def logout_page():
  error = None
  if session['logged_in']:
      session['logged_in'] = False
      flash('You were logged out')
      return redirect(url_for('index'))
  else:
      error = "You have needed to be logged in to log out"
  return render_template('login.html', error=error)

# Editing, Creating, Deleting Posts
@app.route('/edit/<slug>')
def edit_post():
    pass

# this is the main fucntion. 
# Make sure to set debug to False in production.
if __name__ == '__main__':
   app.run(debug=True)
