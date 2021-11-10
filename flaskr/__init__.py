# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2021/05/15 11:37:05
@Author  :   文静静 and 肖中遥 and 余樱童 and 朱韵
@Version :   1.0
@Contact :   lookingforteachers@126.com
'''

import os
from flask import Flask, request, config, jsonify, url_for, render_template, redirect
from flask import flash, session
from flask_sqlalchemy import SQLAlchemy
import json
import time
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField, TextField, form
from wtforms.validators import DataRequired, Length
from wtforms.fields import *

'''
written by: 肖中遥

'''
test_config = None
# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'flaskr.sqlite')
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)
# print("数据库地址 ", os.path.join(app.instance_path, 'flaskr.sqlite'))
db = SQLAlchemy(app)
db_session = db.session
if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass


# 老师类
class Teachers(db.Model):
    '''
    written by: 文静静

    '''
    id = db.Column(db.Integer, primary_key=True)
    tname = db.Column(db.String(80), unique=True)
    college = db.Column(db.String(120), unique=False)
    score = db.Column(db.SmallInteger, unique=False)
    Intro = db.Column(db.String(120), unique=False)
    ScorePeopleNum = db.Column(db.Integer, unique=False)
    CommentNum = db.Column(db.Integer, unique=False)
    UpdateTime = db.Column(db.TEXT, unique=False)
    ResearchInterests = db.Column(db.TEXT, unique=False)
    Title = db.Column(db.TEXT, unique=False)
    AuditState = db.Column(db.SmallInteger)
    

    def __repr__(self):
        return self.title

# 公告类
class Announcement(db.Model):
    '''
    written by: 文静静

    '''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.TEXT, unique=False)
    content = db.Column(db.TEXT, unique=False)
    UploadTime = db.Column(db.TEXT, unique=False)
    Uploader = db.Column(db.TEXT, unique=False)

    def __repr__(self):
        return self.title

# 评论类
class Comments(db.Model):
    '''
    written by: 文静静

    '''
    id = db.Column(db.Integer,autoincrement = True, primary_key=True)
    UploadTime = db.Column(db.TEXT, unique=False)
    TId = db.Column(db.Integer)
    Score = db.Column(db.SmallInteger, unique=False)
    Content = db.Column(db.TEXT, unique=False)
    AuditState = db.Column(db.SmallInteger, unique=False)

    def __repr__(self):
        return self.tname

class Admins(db.Model):
    '''
    written by: 余樱童

    '''
    Account = db.Column(db.TEXT, primary_key=True)
    AdminPassword = db.Column(db.TEXT, nullable=False)

# 主页
@app.route("/index", methods=['post', 'get'])
def index():
    '''
    written by: 肖中遥

    '''
    global names
    if request.method == 'GET':
        return render_template('index.html')
    else:
        content = request.form.get('content')
        # 没有要跳转的页面
        if content is None:
            content = request.form.get('value')  # 获得要查找的老师姓名（可能为空）
            names = []
            if content is not None and content != "":
                quotes = Teachers.query.filter(Teachers.tname.like("%" + content + "%"),Teachers.AuditState != 0).all()
                for quote in quotes:
                    if quote.AuditState == 1:
                        names.append(quote.tname)
            return jsonify(json_list=names)
        # 提交了一个跳转的老师姓名
        else:
            quote = Teachers.query.filter(Teachers.tname == content,Teachers.AuditState != 0).first()
            if quote is None:
                return redirect(url_for('NotFound'))
            else:
                return redirect(url_for('TeacherInformation', teacherName=content))

@app.route("/OverviewTeachers", methods=['POST', 'GET'])
def OverviewTeachers():
    '''
    written by: 肖中遥

    '''
    names = []
    if request.method == 'GET':
        return render_template('OverviewTeachers.html')
    else:
        content = request.form.get('getName')
        if content is None :
            # 测试用，不过滤未过审老师
            # quotes = Teachers.query.all()
            quotes = Teachers.query.filter(Teachers.AuditState == 1).all()
            for quote in quotes:
                names.append(quote.tname)
            return jsonify(json_list=names)
        else:
            return redirect(url_for('TeacherInformation', teacherName=content))

# 显示老师
@app.route("/TeacherInformation/?<string:teacherName>", methods=['POST', 'GET'])
def TeacherInformation(teacherName):
    '''
    written by: 文静静

    '''
    quote = Teachers.query.filter(Teachers.tname == teacherName).first()
    info = []
    info.append(quote.tname)
    info.append(quote.college)
    info.append(quote.score)
    info.append(quote.Intro)
    info.append(quote.Title)
    info.append(quote.ResearchInterests)
    tid = quote.id
    if request.method == 'GET':
        return render_template('TeacherInformation.html', teacher=info)
    else:
        content = request.form.get('id')
        # print(content)
        if content is None:
            message = request.form.get('message')
            if message is None:
                # 测试用，不过滤未过审评论
                # quotes_time = Comments.query.order_by(Comments.UploadTime.desc()).filter(tid == Comments.TId).all()
                # quotes_score = Comments.query.order_by(Comments.Score.desc()).filter(tid == Comments.TId).all()

                quotes_time = Comments.query.order_by(Comments.UploadTime.desc()).filter(tid == Comments.TId, Comments.AuditState == 1).all()
                quotes_score = Comments.query.order_by(Comments.Score.desc()).filter(tid == Comments.TId, Comments.AuditState == 1).all()
                data = {}
                data["id0"] = []
                data["score0"] = []
                data["content0"] = []
                data["uploadtime0"] = []
                data["id1"] = []
                data["score1"] = []
                data["content1"] = []
                data["uploadtime1"] = []
                for q in quotes_time:
                    data["id0"].append(q.id)
                    data["score0"].append(q.Score)
                    data["content0"].append(q.Content)
                    data["uploadtime0"].append(q.UploadTime)

                for q in quotes_score:
                    data["id1"].append(q.id)
                    data["score1"].append(q.Score)
                    data["content1"].append(q.Content)
                    data["uploadtime1"].append(q.UploadTime)
                return jsonify(json_list=data)
            else:
                localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                try:
                    comment = Comments(TId=tid, Content=message, Score=0
                                    , AuditState=0, UploadTime=localtime)
                    db_session.add(comment)
                    db_session.commit()
                except Exception as e:
                    # 加入数据库commit提交失败，必须回滚！！！
                    db_session.rollback()
                    raise e
                return redirect(url_for('TeacherInformation', teacherName=quote.tname))
        else:
            isadd = request.form.get('isadd')
            # print("id:",content)
            quote_comment = Comments.query.filter(Comments.id == content).first()
            temp = quote_comment.Score
            if isadd == '1':
                quote_comment.Score = temp + 1
            else:
                quote_comment.Score = temp - 1
            db_session.commit()
            return redirect(url_for('TeacherInformation', teacherName=quote.tname))


# 公告
@app.route("/Announcements", methods=['POST', 'GET'])
def Announcements():
    '''
    written by: 文静静

    '''
    data = {}
    data["title"] = []
    data["content"] = []
    data["uploadtime"] = []
    data["uploader"] = []
    if request.method == 'GET':
        return render_template('Announcements.html')
    else:
        quotes = Announcement.query.order_by(Announcement.UploadTime.desc()).all()
        for quote in quotes:
            data["title"].append(quote.title)
            data["content"].append(quote.content)
            data["uploadtime"].append(quote.UploadTime)
            data["uploader"].append(quote.Uploader)
        return jsonify(json_list=data)

@app.route("/AboutUs")
def AboutUs():
    return render_template('AboutUs.html')

@app.route("/NotFound")
def NotFound():
    return render_template('NotFound.html')

@app.route("/AddTeacher",methods=['post', 'get'])
def AddTeacher():
    '''
    written by: 文静静

    '''
    print("添加老师")
    if request.method == 'GET':
        return render_template('AddTeacher.html')
    else:
        name = request.form.get('name')
        college = request.form.get('college')
        title = request.form.get('title')
        subject = request.form.get('subject')
        message = request.form.get('message')
        localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # 同一老师已存在，提交失败
        quote =  Teachers.query.filter(Teachers.tname == name,Teachers.college == college,Teachers.Title == title).all()
        if len(quote) != 0:
            return redirect(url_for('AlreadyExist'))
        # 这里要改日期格式
        try:
            teacher = Teachers(tname=name, college = college,ScorePeopleNum = 0,CommentNum = 0, Title=title, ResearchInterests = subject,Intro = message
                            ,AuditState = 0,UpdateTime = localtime, score = 0)
            # Teachers.query.filter(Teachers.tname == name).delete()
            db_session.add(teacher)
            db_session.commit()
        except Exception as e:
            # 加入数据库commit提交失败，必须回滚！！！
            db_session.rollback()
            raise e
        return redirect(url_for('OverviewTeachers'))

@app.route("/AlreadyExist")
def AlreadyExist():
    return render_template('AlreadyExist.html')

# 登录页面表单
class Login(FlaskForm):
    '''
    written by: 余樱童

    '''
    Account = StringField(
        validators=[
            DataRequired('Account could not be empty')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '账号',
            'required': '',
            'autofocus': '',
            'autocomplete':'on'
        }
    )
    Password =PasswordField(
        validators=[
            DataRequired('Password could not be empty')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '密码',
            'autofocus': ''
        }
    )

@app.route("/SignIn", methods=['POST', 'GET'])
def SignIn():
    '''
    written by: 余樱童

    '''
    # del_form=delete()
    # up_form=update()
    if request.method == 'GET':
        form=Login()
    else:
        form = Login(request.form)
        input_account = request.form.get('Account')
        input_password = request.form.get('Password')
        account = Admins.query.filter(Admins.Account == input_account).first()
        if account is not None:  # 存在这个ID
            if account.AdminPassword == input_password:  # 如果密码正确
                session['AdminAccount'] = account.Account
                return redirect(url_for('AdminsPage', AdminsAccount = account.Account))
            else:  # 密码错误
                flash("Wrong password!")
        else:  # ID错误
            flash("Wrong Account!")
    return render_template('SignIn.html', form = form)

# 管理员页面表单
class Admin(FlaskForm):
    '''
    written by: 余樱童 and 朱韵

    '''
    Title = StringField(
        render_kw={
            'class': 'form-control',
            'placeholder': '标题',
            'required': '',
            'autofocus': '',
            'autocomplete':'off'
        }
    )
    Content = StringField(
        render_kw={
            'class': 'form-control',
            'placeholder': '内容',
            'required': '',
            'autofocus': '',
            'autocomplete':'off'
        }
    )
    
# 管理员页面
@app.route("/AdminsPage/?<string:AdminsAccount>", methods=['POST', 'GET'])
def AdminsPage(AdminsAccount):
    '''
    written by: 余樱童 and 朱韵

    '''
    print(AdminsAccount)
    if request.method == 'GET':
        return render_template('AdminsPage.html', AdminsAccount = AdminsAccount)
    elif request.method == 'POST':
        if request.form.get('delcomment') is not None:
            print("删除评论")
            comment_id = int(request.form.get('delcomment')[5:])
            print(comment_id)
            del_sql="DELETE FROM Comments WHERE Id = " + str(comment_id) + ";"
            try:
                db_session.execute(del_sql)
                db_session.commit()
            # 删除和更新过程失败时，回滚
            except:
                db_session.rollback()
                # flash("Delete unsuccessfully!")
            return redirect(url_for('AdminsPage', AdminsAccount = session['AdminAccount']))
        if request.form.get('upcomment') is not None:
            print("更新评论")
            comment_id = int(request.form.get('upcomment')[5:])
            # print(comment_id)
            up_sql = "UPDATE Comments SET AuditState = 1 WHERE Id = " + str(comment_id) + ";"
            # print(up_sql)
            try:
                db_session.execute(up_sql)
                db_session.commit()
            except:  # 删除和更新过程失败时，回滚
                db_session.rollback()
                # flash("Delete unsuccessfully!")
            return redirect(url_for('AdminsPage', AdminsAccount = session['AdminAccount']))
        if request.form.get('delteacher') is not None:
            teacher_id = int(request.form.get('delteacher')[5:])
            # print(teacher_id)
            del_sql="DELETE FROM Teachers WHERE Id = " + str(teacher_id) + ";"
            try:
                db_session.execute(del_sql)
                db_session.commit()
            # 删除和更新过程失败时，回滚
            except:
                db_session.rollback()
                # flash("Delete unsuccessfully!")
            return redirect(url_for('AdminsPage', AdminsAccount = session['AdminAccount']))
        if request.form.get('upteacher') is not None:
            teacher_id = int(request.form.get('upteacher')[5:])
            # print(teacher_id)
            up_sql = "UPDATE Teachers SET AuditState = 1 WHERE Id = " + str(teacher_id) + ";"
            # print(up_sql)
            try:
                db_session.execute(up_sql)
                db_session.commit()
            except:  # 删除和更新过程失败时，回滚
                db_session.rollback()
                # flash("Delete unsuccessfully!")
            return redirect(url_for('AdminsPage', AdminsAccount = session['AdminAccount']))
        if request.form.get('getdata') is not None:
            if request.form.get('getdata') == 'comment':
                quotes_comment = Comments.query.order_by(Comments.UploadTime.asc()).filter(Comments.AuditState == 0).all()
                data = {}
                data["content0"] = []
                data["uploadtime0"] = []
                data["CID"] = []
                data["TID0"] = []
                data["Tname0"] = []
                for q in quotes_comment:
                    data["content0"].append(q.Content)
                    data["uploadtime0"].append(q.UploadTime)
                    data["CID"].append(q.id)
                    data["TID0"].append(q.TId)
                    this_teacher = Teachers.query.filter(Teachers.id == q.TId).first()
                    data["Tname0"].append(this_teacher.tname)
                return jsonify(json_list=data)
            elif request.form.get('getdata') == 'teacher':
                quotes_teachers = Teachers.query.order_by(Teachers.UpdateTime.desc()).filter(Teachers.AuditState == 0).all()
                data = {}
                data["Tname1"] = []
                data["College1"] = []
                data["Intro1"] = []
                data["UpdateTime1"] = []
                data["ResearchInterests1"] = []
                data["Title1"] = []
                data["TID1"] = []
                for q in quotes_teachers:
                    data["Tname1"].append(q.tname)
                    data["College1"].append(q.college)
                    data["Intro1"].append(q.Intro)
                    data["UpdateTime1"].append(q.UpdateTime)
                    data["ResearchInterests1"].append(q.ResearchInterests)
                    data["Title1"].append(q.Title)
                    data["TID1"].append(q.id)
                return jsonify(json_list=data)
        #发布公告
        if request.form.get('announceTitle') is not None:
            announceTitle=request.form.get('announceTitle')
            announcement=request.form.get('announcement')
            localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            if len(announceTitle)!=0 and len(announcement)!=0:
                try:
                    announce=Announcement(title=announceTitle,content=announcement,
                                        UploadTime=localtime,Uploader=AdminsAccount)
                    db_session.add(announce)
                    db_session.commit()
                except Exception as e:
                    db_session.rollback()
                    raise e
        return redirect(url_for('AdminsPage', AdminsAccount = session['AdminAccount']))

# a simple page that says hello
# just for test
@app.route('/hello')
def hello():
    return 'Hello, World!'

from . import database
database.init_app(app)