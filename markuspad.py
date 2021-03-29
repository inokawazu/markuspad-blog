from flask import (Flask, render_template, session, 
                   request, flash, redirect, url_for)

DATABASE = './blog.db'
SECRET_KEY = 'sample key'
USERNAME = 'user'
PASSWORD = 'bananacar'
DEBUG = True

# Create App
app = Flask(__name__)
app.config.from_object(__name__)

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

#Session - (Inspired by https://github.com/QuadPiece/flask-blog/blob/master/exec.py)
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
