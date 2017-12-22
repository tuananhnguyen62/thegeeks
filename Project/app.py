from flask import *
import mlab
from mongoengine import *
from random import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "Csb~a J]?E3z_mx"
mlab.connect()

class Question_Sample(Document):
    question_content = StringField()

class Question(Document):
    content = StringField()
    username = StringField()
    answer1 = StringField()
    answer2 = StringField()
    answer3 = StringField()
    answer4 = StringField()
    right_answer = StringField()

class User(Document):
    username = StringField()
    user_password = StringField()


class Tree(Document):
    name_tree = StringField()
    password = StringField()

@app.route('/add_question_sample', methods=['GET', 'POST'])
def add_question_sample():
    if request.method == "GET":
        return render_template('add_question_sample.html')
    elif request.method == "POST":
        form = request.form
        question_content = form['question_content']
        new_Question_Sample = Question_Sample(question_content= question_content)
        new_Question_Sample.save()
        return render_template('/add_question_sample.html')

@app.route('/create_tree', methods=['GET', 'POST'])
def create_tree():
    if request.method == "GET" :
        return render_template('create_tree.html')
    elif request.method == "POST" :
        form = request.form
        name_tree = form['name_tree']
        password = form['password']
        new_tree = Tree(name_tree=name_tree, password=password)
        new_tree.save()
        return redirect(url_for('create_tree_2'))

@app.route('/create_tree_2', methods=['GET', 'POST'])
def create_tree_2():
    if request.method == "GET" :
        return render_template('create_tree_2.html')
    elif request.method == "POST" :
        form = request.form
        username = form['username']
        user_password = form['user_password']
        new_user = User(username=username, user_password= user_password)
        new_user.save()
        return render_template('create_tree_2.html')

@app.route('/join', methods = ['GET', 'POST'])
def join():
    if request.method == 'GET':
        return render_template('join_group.html')
    elif request.method == 'POST':
        form = request.form
        name_tree = form['name_tree']
        password = form['password']
        print(name_tree)
        print(password)
        tree = Tree.objects(name_tree = name_tree).first()
        if tree is None:
            return 'Nhóm Không tồn tại'
        elif tree.password != password :
            return "Password sai, nhập lại"
        else:
            return redirect(url_for('input_member'))
@app.route('/input_member', methods = ['GET', 'POST'])
def input_member():
    if request.method == 'GET':
        return render_template('join_group_2.html')
    elif request.method == 'POST':
        form = request.form
        username = form['username']
        user_password = form['user_password']
        user = User.objects(username = username).first()
        if user is None:
            return "username không tồn tại"
        elif user.user_password != user_password:
            return "Password sai"
        else:
            # session['loggedin'] = True
            return "Đăng nhập thành công"

@app.route('/create_question',methods = ['GET', 'POST'])
def create_question():
    question_sample = Question_Sample.objects()
    question_random = choice(question_sample)
    if request.method == "GET":
        return render_template('create_question.html', question_contents= question_random["question_content"])
    elif request.method == "POST":
        content = question_random["question_content"]
        form = request.form
        username = form['username']
        answer1 = form['answer1']
        answer2 = form['answer2']
        answer3 = form['answer3']
        answer4 = form['answer4']
        right_answer = form['right_answer']
        new_question = Question(content=content, username=username, answer1=answer1, answer2=answer2, answer3=answer3, answer4=answer4, right_answer= right_answer)
        new_question.save()
        return "Tạo câu hỏi thành công"

@app.route('/show_question', methods = ['GET', 'POST'])
def show_question():
    question_show = Question.objects()
    question_show_random = choice(question_show)
    if request.method == 'GET':
        # return question_show_random.content
        return render_template('show_question.html', answer_shows = question_show_random)
    elif request.method == 'POST':
        form = request.form
        right_answer = form['right_answer']
        if right_answer == question_show_random.right_answer:
            return "Đúng, cộng 1 điểm"
        else:
            return "Chúc bạn may mắn lần sau"

@app.route('/')
def index():
    loggedin = session.get('loggedin', False)
    return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        form = request.form
        username = form['username']
        password = form['password']
        user = User.objects(username=username).first()
        if user is None:
            return "User không tồn tại"
        elif user.password != password:
            return "Sai password"
        else:
            session['loggedin'] = True
            return redirect(url_for('admin'))


if __name__ == '__main__':
  app.run(debug=True)
