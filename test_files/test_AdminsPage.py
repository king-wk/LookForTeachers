'''
@File    :   test_AdminsPage.py
@Time    :   2021/07/10
@Author  :   余樱童
@Version :   1.0
@Contact :   lookingforteachers@126.com
'''

from PackagesandModules import *
from test_login import login

@pytest.fixture
def client():
    db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True

    with flaskr.app.test_client() as client:
        with flaskr.app.app_context():
            init_db()
            # flaskr.database.init_db()
        yield client

    os.close(db_fd)
    os.unlink(flaskr.app.config['DATABASE'])


def AdminsPage(client, path, delcomment=None, upcomment=None, delteacher=None, upteacher=None, getdata=None, announceTitle=None, announcement=None):
    return client.post(path, data=dict(
        delcomment=delcomment,
        upcomment=upcomment,
        delteacher=delteacher,
        upteacher=upteacher,
        getdata=getdata,
        announceTitle=announceTitle,
        announcement=announcement
    ), follow_redirects=False)

def login(client, username, password):
    return client.post('/SignIn', data=dict(
        Account=username,
        Password=password
    ), follow_redirects=True)

def test_AdminsPage(client):
    """Make sure index page works."""

    username = "admin001"
    password = "helloworld"

    exist_teachername = "程明明"
    none_teachername = "张莹"
    college = "计算机学院"
    title = "教授"

    rv = login(client, username, password)
    assert flask.session['AdminAccount'] == username
    assert flask.request.path == "/AdminsPage/?" + username

    print("登录")

    real_path = "/AdminsPage/%3F" + username
    path = "/AdminsPage/?" + username

    # 评论审核未通过
    resp = AdminsPage(client, real_path, "评论编号：18")
    assert flask.request.path == path
    print("未通过")

    # 评论审核通过
    resp = AdminsPage(client, real_path, None, "评论编号：3")
    assert flask.request.path == path

    # 老师审核未通过
    resp = AdminsPage(client, real_path, None, None, "老师编号：1")
    assert flask.request.path == path

    # 老师审核通过
    resp = AdminsPage(client, real_path, None, None, None, "老师编号：2")
    assert flask.request.path == path

    # 获取评论数据
    resp = AdminsPage(client, real_path, None, None, None, None, "comment")
    data = json.loads(resp.data)
    # 上面对评论的操作确实有效
    assert 3 not in data['json_list']["CID"]
    assert 18 not in data['json_list']["CID"]
    assert 22 in data['json_list']["CID"]

    # 获取老师数据
    resp = AdminsPage(client, real_path, None, None, None, None, "teacher")
    data = json.loads(resp.data)
    # 上面对老师的操作确实有效
    assert 1 not in data['json_list']["TID1"]
    assert 2 not in data['json_list']["TID1"]
    assert 4 in data['json_list']["TID1"]

    # 发布公告
    resp = AdminsPage(client, real_path, None, None, None, None, None, "测试公告", "这是一个测试公告")
    assert flask.request.path == path
    # 该部分对数据库运行的结果可以直接到数据库中查看