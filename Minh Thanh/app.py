from flask import *
from mongoengine import *
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-tree')
def sign_in():
    return render_template('create_tree.html')

@app.route('/about-me')
def about_me():
    return render_template('about_me.html')
@app.route('/create-tree-2')
def add_member():
    return render_template('create_tree_2.html')
if __name__ == '__main__':
  app.run(debug=True)
