"""The DB models."""
from datetime import datetime

from flask_security import RoleMixin, UserMixin

from iris import db


class LectureSession(db.Model):
    """Represents a single lecture session."""

    __tablename__ = 'lecturesession'
    session_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    active = db.Column(db.Boolean, default=False)

    def __init__(self, course_id):
        """Create a new lecturesession, connected to course_id."""
        self.course_id = course_id

    def __repr__(self):
        """A textual representation of the class."""
        return '<LSession status: {}>'.format(self.active)


class SessionFeedback(db.Model):
    """Represents the number of times an action has been received."""

    __tablename__ = 'sessionfeedback'
    session_id = db.Column(db.Integer,
                           db.ForeignKey('lecturesession.session_id'),
                           primary_key=True)
    action_name = db.Column(db.String, primary_key=True)
    count = db.Column(db.Integer, default=0)

    def __init__(self, session_id, action_name):
        """Create a new feedback, connected to session_id."""
        self.session_id = session_id
        self.action_name = action_name

    def __repr__(self):
        """A textual representation of the class."""
        return '<SFeedback for {} - {}: {}'.format(self.session_id,
                                                   self.action_name,
                                                   self.count)


class Questions(db.Model):
    """Represents asked questions."""

    __tablename__ = 'questions'
    question_id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer,
                           db.ForeignKey('lecturesession.session_id'))
    question = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    answered = db.Column(db.Boolean, default=False)
    flagged = db.Column(db.Boolean, default=False)

    def __init__(self, session_id, question):
        """Create a new question, connected to session_id."""
        self.session_id = session_id
        self.question = question
        self.timestamp = datetime.utcnow()

    def __repr__(self):
        """A textual representation of the class."""
        return '<Question {} for session {}: {} >'.format(self.question_id,
                                                          self.session_id,
                                                          self.question)


courses_users = db.Table('courses_users',
                         db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                         db.Column('course_id', db.Integer(), db.ForeignKey('course.id')))


class Course(db.Model, RoleMixin):
    """Represents courses."""

    __tablename__ = 'course'
    id = db.Column(db.Integer(), primary_key=True)
    code = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    """Represents users."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Course', secondary=courses_users,
                            backref=db.backref('users', lazy='dynamic'))
