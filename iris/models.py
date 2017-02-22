from iris import db


class LectureSession(db.Model):
    __tablename__ = 'lecturesession'
    session_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer)
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
