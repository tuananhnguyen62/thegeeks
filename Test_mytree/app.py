from flask import *
import mlab
from mongoengine import *
app = Flask(__name__)

mlab.connect()

class Group(Document):
    group_name = StringField()
    member1 = StringField()
    member2 = StringField()
    member3 = StringField()
    member4 = StringField()
    member5 = StringField()
    member6 = StringField()
    point = IntField()

# new_group = Group(
#     group_name = "The Geeks",
#     member1 = "Nam Phong",
#     member2 = "Tuan Anh",
#     member3 = "Cuong",
#     member4 = "Thanh",
#     member5 = "Hung",
#     member6 = "StringField()",
#     point = 15
# )
# new_group.save()
# items = Group.objects()
# @app.route('/my_tree/<item_id>')
# @app.route('/')
# # def index(item_id):
#     items = Group.objects().with_id(item_id)
#     return render_template('my_tree.html', items= items)
@app.route('/')
def index():
    items = Group.objects()
    return render_template('my_tree.html', items=items)

if __name__ == '__main__':
  app.run(debug=True)
