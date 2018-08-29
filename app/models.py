from app import db
from app import login
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    grade_reports = db.relationship('GradeReport', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


@login.user_loader
def load_user(m_id):
    return User.query.get(int(m_id))


class GradeReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(500))
    session_course = db.Column(db.String(20))
    date_report = db.Column(db.DateTime, index=True)
    date_creation = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tests_names = db.Column(db.String(500))
    a_grade = db.Column(db.String(500))
    b_grade = db.Column(db.String(500))
    c_grade = db.Column(db.String(500))
    f_grade = db.Column(db.String(500))

    def __repr__(self):
        return 'Курс "{}", запуск {}'.format(self.course_name, self.session_course)


class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(240))
    course = db.relationship('CourseList', backref='plat_name', lazy='dynamic')

    def __repr__(self):
        return 'Платформа: {}'.format(self.name)


class CourseList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(100))
    course_name = db.Column(db.String(500))
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))
    session = db.relationship('SessionList', backref='course_name', lazy='dynamic')

    def __repr__(self):
        return 'Курс: {} - {}'.format(self.course_code, self.course_name)


class SessionList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_name = db.Column(db.String(100))
    session_start_date = db.Column(db.Date, index=True)
    session_end_date = db.Column(db.Date, index=True)
    id_course_name = db.Column(db.Integer, db.ForeignKey('course_list.id'))
    session_info = db.relationship('SessionInfo', backref='session_name', lazy='dynamic')

    def __repr__(self):
        return 'Сессия: {}'.format(self.session_name)


class SessionInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_session = db.Column(db.Integer, db.ForeignKey('session_list.id'))
    count_students = db.Column(db.Integer)
    count_verified = db.Column(db.Integer)
    count_students_urfu = db.Column(db.Integer)

    def __repr__(self):
        return 'Подробная информация о сессии: {}'.format(self.id_session)
