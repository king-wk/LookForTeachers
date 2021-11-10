'''
@File    :   test_login.py
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
            # flaskr.db.init_db()
        yield client

    os.close(db_fd)
    os.unlink(flaskr.app.config['DATABASE'])


def login(client, username, password):
    return client.post('/SignIn', data=dict(
        Account=username,
        Password=password
    ), follow_redirects=True)

def test_login_logout(client):
    """Make sure login works."""

    username = "admin001"
    password = "helloworld"

    # 正常登录
    rv = login(client, username, password)
    assert flask.session['AdminAccount'] == username
    assert flask.request.path == "/AdminsPage/?" + username

    # 用户名错误
    rv = login(client, f"{username}x", password)
    assert flask.request.path == "/SignIn"

    # 密码错误
    rv = login(client, username, f'{password}x')
    assert flask.request.path == "/SignIn"