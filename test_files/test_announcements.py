'''
@File    :   test_announcements.py
@Time    :   2021/07/10
@Author  :   朱韵
@Version :   1.0
@Contact :   lookingforteachers@126.com
'''

from PackagesandModules import *

@pytest.fixture
def client():
    db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True

    with flaskr.app.test_client() as client:
        with flaskr.app.app_context():
            init_db()
            # flaskr.db.init_db()
        yield client

    os.close(db_fd)
    os.unlink(flaskr.app.config['DATABASE'])

def Announcements(client):
    return client.post("/Announcements", follow_redirects=True)

def test_announcements(client):
    resp = Announcements(client)
    data = json.loads(resp.data)
    assert data['json_list']['title'][-1]=="召唤管理员"
