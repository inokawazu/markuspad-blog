from flask import Flask, render_template
app = Flask(__name__)

# This is the home-page
@app.route('/')
def index():
   return render_template('index.html')

# this is the main fucntion. 
# Make sure to set debug to False in production.
if __name__ == '__main__':
   app.run(debug=True)
