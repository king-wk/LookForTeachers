# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2021/05/15 11:37:05
@Author  :   肖中遥
@Version :   1.0
@Contact :   lookingforteachers@126.com
'''
class Teacher(object):

    def __init__(self):
        self._score = 0
        self._id = 0
        self._name = ''
        self._information = ''
        self._college = ''
        self._num_comment = 0
        self._num_commentator = 0
        self._last_update_time = ''
        self._lectures = []
        self._comments = []

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    # 依次类推，按需求写get和set方法


class Lecture(object):
    def __init__(self):
        self._id = 0
        self._name = ''
        self._open_unit = ''
        self._open_time = ''
        self._open_count = ''
        self._update_time = ''
        self._teachers = []


class Comment(object):
    def __init__(self):
        self._id = id
        self._score = 0
        self._teacher_id = 0
        self._time = ''


class Administor(object):
    def __init__(self):
        self._account = ''
        self._password = ''

    def login_in(self, acc, pa):
        return 0
