import mongoengine

# mongodb://<dbuser>:<dbpassword>@ds163806.mlab.com:63806/mytree_data_test

host = "ds163806.mlab.com"
port = 63806
db_name = "mytree_data_test"
user_name = "admin"
password = "admin"
# Authentication failed: lỗi bảo mật


def connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())
