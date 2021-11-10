'''
@File    :   test_index.py
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

    with flaskr.app.test_client() as client:
        with flaskr.app.app_context():
            init_db()
            # flaskr.database.init_db()
        yield client

    os.close(db_fd)
    os.unlink(flaskr.app.config['DATABASE'])


def index(client, content, value):
    return client.post('/index', data=dict(
        content=content,
        value=value
    ), follow_redirects=True)

def test_index(client):
    """Make sure index page works."""

    teachername = "程明明"

    # 查找老师
    resp = index(client, None, teachername)
    data = json.loads(resp.data)
    assert data['json_list'] == [teachername]

    # 跳转页面
    # 存在该老师
    resp = index(client, teachername, teachername)
    assert flask.request.path == "/TeacherInformation/?" + teachername
    # 不存在该老师
    resp = index(client, "helloworld", teachername)
    assert flask.request.path == '/NotFound'