from datetime import datetime

from flask_security import RoleMixin, UserMixin

from iris import db


class LectureSession(db.Model):
    __tablename__ = 'lecturesession'
    session_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    active = db.Column(db.Boolean, default=False)

    def __init__(self, course_id):
        self.course_id = course_id

    def __repr__(self):
        return '<LSession status: {}>'.format(self.active)


class SessionFeedback(db.Model):
    __tablename__ = 'sessionfeedback'
    session_id = db.Column(db.Integer,
                           db.ForeignKey('lecturesession.session_id'),
                           primary_key=True)
    action_name = db.Column(db.String, primary_key=True)
    count = db.Column(db.Integer, default=0)

    def __init__(self, session_id, action_name):
        self.session_id = session_id
        self.action_name = action_name

    def __repr__(self):
        return '<SFeedback for {} - {}: {}'.format(self.session_id,
                                                   self.action_name,
                                                   self.count)


class Questions(db.Model):
    __tablename__ = 'questions'
    question_id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer,
                           db.ForeignKey('lecturesession.session_id'))
    question = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    answered = db.Column(db.Boolean, default=False)
    flagged = db.Column(db.Boolean, default=False)

    def __init__(self, session_id, question):
        self.session_id = session_id
        self.question = question
        self.timestamp = datetime.utcnow()

    def __repr__(self):
        return '<Question {} for session {}: {} >'.format(self.question_id,
                                                          self.session_id,
                                                          self.question)


courses_users = db.Table('courses_users',
                         db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                         db.Column('course_id', db.Integer(), db.ForeignKey('course.id')))


class Course(db.Model, RoleMixin):
    __tablename__ = 'course'
    id = db.Column(db.Integer(), primary_key=True)
    code = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Course', secondary=courses_users,
                            backref=db.backref('users', lazy='dynamic'))
