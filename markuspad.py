from flask import (Flask, render_template, session, 
                   request, flash, redirect, url_for, abort)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from slugify import slugify

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
    slug = db.Column(db.String(80), nullable=False, unique = True)
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
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return '<Category %r>' % self.name

# This is the home-page
@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts = posts, categories=get_all_categories())

# This is the about-page
@app.route('/about')
def about_page():
   return render_template('about.html', categories=get_all_categories())

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error, categories=get_all_categories()), 404

#Session(login and logout) - (Inspired by https://github.com/QuadPiece/flask-blog/blob/master/exec.py)
@app.errorhandler(403)
def page_access_denied(error):
    return render_template('403.html', error=error, categories=get_all_categories()), 403

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
  return render_template('login.html', error=error, categories=get_all_categories())

@app.route('/logout')
def logout_request():
  error = None
  if session['logged_in']:
      session['logged_in'] = False
      flash('You were logged out')
      return redirect(url_for('index'))
  else:
      error = "You have needed to be logged in to log out"
  return render_template('login.html', error=error, categories=get_all_categories())

# # Editing, Creating, Deleting Posts
# @app.route('/edit')
# def see_editable():
#     if not session['logged_in']:
#         return abort(403)
#     return "EDIT - " + str(session['logged_in'])

@app.route('/edit/<slug>', methods=['GET', 'POST'])
def editpost(slug):
    #checked if logged in
   if not session['logged_in']:
       return abort(403)

   #find the entry
   post = Post.query.filter_by(slug=slug).first()

   #check if entry was found
   if not post:
       return abort(404)

   if request.method == 'POST':
       for entry in ['title','slug','body', 'category']:
           if not request.form[entry]:
               flash("Please enter a correct {}".format(entry))
               return render_template('make_edits.html', post=post, action='/edit/'+slug, categories=get_all_categories())

       slug_cat = slugify(request.form['category'])
       category = Category.query.filter_by(name=slug_cat).first()
       if not category:
           category = Category(name=slug_cat)

       post.title = request.form['title']
       post.slug = slugify(request.form['slug'])
       post.body = request.form['body']
       post.category = category
       db.session.commit()

       return redirect(url_for('index'))
   else:
       return render_template('make_edits.html', post=post, action='/edit/'+slug, categories=get_all_categories())

@app.route('/make', methods=['GET', 'POST'])
def createpost():
    #checked if logged in
   if not session['logged_in']:
       return abort(403)

   category = Category(name = "blank")

   post = Post(title = "Title",
               slug = "slug",
               body = "body",
               category = category)

   if request.method == 'POST':
       for entry in ['title','slug','body', 'category']:
           if not request.form[entry]:
               flash("Please enter a correct {}".format(entry))
               return render_template('make_edits.html', post=post, action='/make', 
                                      categories=get_all_categories())

       slug_cat = slugify(request.form['category'])
       category = Category.query.filter_by(name=slug_cat).first()
       if not category:
           category = Category(name=slug_cat)

       post = Post(title = request.form['title'],
                   slug = slugify(request.form['slug']),
                   body = request.form['body'],
                   category = category)
       db.session.add(post)
       db.session.commit()

       return redirect(url_for('index'))
   else:
       return render_template('make_edits.html', post=post, action='/make', categories=get_all_categories())

# This is the view page for categories
@app.route('/<category>')
def category_posts(category):
    posts = Category.query.filter_by(name=category).first_or_404().posts
    return render_template('index.html', posts = posts, categories=get_all_categories())

# This is the view for a particular post.
@app.route('/<category>/<slug>')
def view_post(category,slug):
    filtered_category = Category.query.filter_by(name=category).first_or_404()
    post = Post.query.filter_by(category=filtered_category).filter_by(slug=slug).first_or_404()
    return render_template('view_post.html', post=post, categories=get_all_categories())

#Util Functions
def get_all_categories():
    return Category.query.all()

# this is the main fucntion. 
# Make sure to set debug to False in production.
if __name__ == '__main__':
   app.run(debug=True)
