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
    name_tree  = StringField()
    content = StringField()
    username = StringField()
    answer1 = StringField()
    answer2 = StringField()
    answer3 = StringField()
    answer4 = StringField()
    right_answer = StringField()

class User(Document):
    name_tree = StringField()
    username = StringField()
    user_password = StringField()


class Tree(Document):
    name_tree = StringField()
    password = StringField()
    point = IntField()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_question_sample', methods=['GET', 'POST'])
def add_question_sample():
    if request.method == "GET":
        return render_template('add_question_sample.html')
    elif request.method == "POST":
        form = request.form
        question_content = form['question_content']
        new_Question_Sample = Question_Sample(question_content= question_content)
        new_Question_Sample.save()
        return render_template('add_question_sample.html')

@app.route('/create_tree', methods=['GET', 'POST'])
def create_tree():
    if request.method == "GET" :
        return render_template('create_tree.html')
    elif request.method == "POST" :
        form = request.form
        name_tree = form['name_tree']
        password = form['password']
        check_tree = Tree.objects(name_tree = name_tree).first()
        if check_tree is None:
            new_tree = Tree(name_tree=name_tree, password=password, point =0)
            new_tree.save()
            session['created_tree'] = True #lưu session tạo tên cây khi khởi tạo
            session['created_name_tree'] = name_tree #lưu thông tin của tên cây khi khởi tạo
            return redirect(url_for('create_tree_2'))
        else:
            return "Tên cây đã được sử dụng"

@app.route('/create_tree_2', methods=['GET', 'POST'])
def create_tree_2():
    if session.get('created_tree', False): #kiểm tra xem đã tọa tên cây trước chưa?
        name_tree = session['created_name_tree']
        if request.method == "GET" :
            return render_template('create_tree_2.html')
        elif request.method == "POST" :
            form = request.form
            username = form['username']
            user_password = form['user_password']
            new_user = User(name_tree=name_tree, username=username, user_password= user_password)
            new_user.save()
            return render_template('create_tree_2.html', name_tree = name_tree)
    else:
        return redirect(url_for('create_tree')) #đưa người dùng về tạo tên cây

@app.route('/join', methods = ['GET', 'POST'])
def join():
    if request.method == 'GET':
        return render_template('join_group.html')
    elif request.method == 'POST':
        form = request.form
        name_tree = form['name_tree']
        password = form['password']
        tree = Tree.objects(name_tree = name_tree).first()
        if tree is None:
            return 'Nhóm Không tồn tại'
        elif tree.password != password :
            return "Password sai, nhập lại"
        else:
            session['loggedin_tree'] = True #xác nhận người dùng đã đăng nhập vào cây
            session['name_tree'] = name_tree #lưu lại thông tin tên Cây của nhóm
            return redirect(url_for('input_member'))

@app.route('/input_member', methods = ['GET', 'POST'])
def input_member():
    if session.get('loggedin_tree', False):   #kiểm tra xem người dùng đã đăng nhập vào cây chưa?
        name_tree = session['name_tree'] #lấy lại thông tin name_tree
        if request.method == 'GET':
            return render_template('join_group_2.html', name_tree= name_tree)
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
                session['loggedin_user'] = True #xác nhận người dùng đã đăng nhập cả vào cây và vào user
                session['username'] = username
                return "Đăng nhập thành công" #cần return đến trang chủ
    else:
        return redirect(url_for('join')) #đưa người dùng quay lại đăng nhập vào cây

@app.route('/create_question',methods = ['GET', 'POST'])
def create_question():
    if session.get('loggedin_tree', False): #kiểm tra xem người dùng đã đăng nhập vào cây chưa?
        if session.get('loggedin_user', False):  #kiểm tra xem người dùng đã đăng nhập vào username chưa?
            name_tree = session['name_tree'] #lấy lại thông tin Cây của nhóm
            username = session['username'] #Lấy lại thông tin của user
            question_sample = Question_Sample.objects()
            question_random = choice(question_sample)
            if request.method == "GET":
                return render_template('create_question.html', question_content= question_random["question_content"], name_tree= name_tree, username= username)
            elif request.method == "POST":
                form = request.form
                name_tree = name_tree
                content = form['content']
                username = username
                answer1 = form['answer1']
                answer2 = form['answer2']
                answer3 = form['answer3']
                answer4 = form['answer4']
                right_answer = form['right_answer']
                new_question = Question(content=content, name_tree= name_tree, username=username, answer1=answer1, answer2=answer2, answer3=answer3, answer4=answer4, right_answer= right_answer)
                new_question.save()
                return "Tạo câu hỏi thành công"
        else:
            return redirect(url_for('input_member')) #đưa người dùng quay lại đăng nhập username
    else:
        return redirect(url_for('join')) #đưa người dùng quay lại đăng nhập vào cây

@app.route('/show_question', methods = ['GET', 'POST'])
def show_question():
    if session.get('loggedin_tree', False): #kiểm tra xem người dùng đã đăng nhập vào cây chưa?
        if session.get('loggedin_user', False): #kiểm tra xem người dùng đã đăng nhập vào username chưa?
            name_tree = session['name_tree'] #lấy lại thông tin Cây của nhóm
            username = session['username'] #Lấy lại thông tin của user
            # point_trees = Tree.objects(name_tree= name_tree).first() #Lấy điểm số của Cây từ database về
            # point_tree = point_trees.point
            # print(point_trees)
            question_show = Question.objects()
            question_show_random = choice(question_show)
            if question_show_random.username != username: #đưa ra điều kiện để username của câu hỏi khác với username hiện tại của người dùng thì mới hiện ra
                if request.method == 'GET':
                    return render_template('show_question.html',username= username ,name_tree= name_tree, answer_shows = question_show_random)
                elif request.method == 'POST':
                    form = request.form
                    right_answer = form['right_answer']
                    if right_answer == question_show_random.right_answer:
                        return "Đúng, cộng 1 điểm. Bạn đã hết lượt trả lời câu hỏi. Xin mời logout và đăng nhập lại để tiếp tục tạo hoặc trả lời câu hỏi nhé!"  #CƠ CHẾ TĂNG ĐIỂM CHO CÂY VÀO ĐÂY!<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!!!!!!!!!!!!!!!!!!
                    else:
                        return "Chúc bạn may mắn lần sau. Bạn đã hết lượt trả lời câu hỏi. Xin mời logout và đăng nhập lại để tiếp tục tạo hoặc trả lời câu hỏi nhé! "
            else:
                return redirect(url_for('show_question_again')) #đưa về trang show_question_again để gen lại câu hỏi khác
        else:
            return redirect(url_for('input_member')) #đưa người dùng quay lại đăng nhập username
    else:
        return redirect(url_for('join')) #đưa người dùng quay lại đăng nhập vào cây

@app.route('/show_question_again')
def show_question_again():
    return render_template('show_question_again.html')


@app.route('/logout')
def logout():
    session['loggedin_tree'] = False
    return redirect(url_for('join')) #đưa người dùng quay lại đăng nhập vào cây

@app.route('/my_tree')
def my_tree():
    if session.get('loggedin_tree', False): #kiểm tra xem người dùng đã đăng nhập vào cây chưa?
        if session.get('loggedin_user', False): #kiểm tra xem người dùng đã đăng nhập vào username chưa?
            name_tree = session['name_tree'] #lấy lại thông tin Cây của nhóm
            username = session['username'] #Lấy lại thông tin của user
        else:
            return redirect(url_for('input_member')) #đưa người dùng quay lại đăng nhập username
    else:
        return redirect(url_for('join')) #đưa người dùng quay lại đăng nhập vào cây


if __name__ == '__main__':
  app.run(debug=True)
