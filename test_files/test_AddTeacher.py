'''
@File    :   test_AddTeacher.py
@Time    :   2021/07/10
@Author  :   余樱童
@Version :   1.0
@Contact :   lookingforteachers@126.com
'''

from PackagesandModules import *

@pytest.fixture
def client():
    print("进入client")
    db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True
    print(flaskr.app.config['DATABASE'])

    with flaskr.app.test_client() as client:
        with flaskr.app.app_context():
            init_db()
            # flaskr.database.init_db()
        yield client

    os.close(db_fd)
    os.unlink(flaskr.app.config['DATABASE'])


def AddTeacher(client, name, college, title, subject, message, localtime):
    return client.post('/AddTeacher', data=dict(
        name=name,
        college=college,
        title=title,
        subject=subject,
        message=message,
        localtime=localtime
    ), follow_redirects=True)

def test_AddTeacher(client):
    """Make sure index page works."""

    exist_teachername = "程明明"
    none_teachername = "张莹"
    college = "计算机学院"
    title = "教授"

    # 要添加的老师已存在
    resp = AddTeacher(client, exist_teachername, college, title, None, None, None)
    assert flask.request.path == '/AlreadyExist'

    # 添加老师
    resp = AddTeacher(client, none_teachername, college, title, "自然语言处理、大数据技术、信息检索、数据挖掘、机器学习", "很好", "2021-07-11 10:47:32")
    assert flask.request.path == '/OverviewTeachers'

    # 添加的老师确实存在了
    resp = AddTeacher(client, none_teachername, college, title, None, None, None)
    assert flask.request.path == '/AlreadyExist'