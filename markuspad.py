from flask import Flask, render_template
app = Flask(__name__)

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

# this is the main fucntion. 
# Make sure to set debug to False in production.
if __name__ == '__main__':
   app.run(debug=True)
