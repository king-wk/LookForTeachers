'''
@File    :   test_teacherinformation.py
@Time    :   2021/07/10
@Author  :   朱韵
@Version :   1.0
@Contact :   lookingforteachers@126.com
'''

from flask.signals import message_flashed
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

def teacherinformation_get(client, teacher_name):
    requestPath = "/TeacherInformation/%3F" + teacher_name
    return client.get(requestPath, follow_redirects=True)

def teacherinformation_post(client, teacher_name,message,isadd):
    requestPath = "/TeacherInformation/%3F" + teacher_name
    return client.post(requestPath, data=dict(
        message = message,
        isadd = isadd
    ), follow_redirects=False)

def test_teacher_info(client):
    """Make sure the infomation of teacher is correct."""
    
    teacher_name="杨征路"

    #根据老师姓名获取老师信息
    resp = teacherinformation_get(client,teacher_name)
    data = str(resp.data,encoding="utf-8")
    assert "杨征路" in data
    assert "人工智能，数据挖掘，信息检索" in data

    #显示评论
    teacher_name="温延龙"
    resp = teacherinformation_post(client,teacher_name,None,None)
    data = json.loads(resp.data)
    assert "龙哥整个人就散发着调皮的气息。。。" in data['json_list']['content0']
    assert data['json_list']['id0'][-1]==5 #最早的评论id号为5

    #提交评论
    message="上龙哥的课很有收获"
    resp = teacherinformation_post(client,teacher_name,message,None)
    data=flask.request.form.get('message')
    assert message==data

    #点踩
    resp=teacherinformation_post(client,teacher_name,None,1)
    assert resp.status_code==200
    assert flask.request.path == "/TeacherInformation/?" + teacher_name