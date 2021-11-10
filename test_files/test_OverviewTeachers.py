'''
@File    :   test_OverviewTeachers.py
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


def OverviewTeachers(client, getName):
    return client.post('/OverviewTeachers', data=dict(
        getName=getName
    ), follow_redirects=True)

def test_OverviewTeachers(client):
    """Make sure index page works."""

    teachername = "程明明"

    # 查找老师
    resp = OverviewTeachers(client, None)
    data = json.loads(resp.data)
    assert teachername in data['json_list']
    assert '卢绍平' not in data['json_list']

    # 跳转页面，返回老师信息
    resp = OverviewTeachers(client, teachername)
    assert flask.request.path == "/TeacherInformation/?" + teachername