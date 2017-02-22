from flask import render_template, redirect, url_for
from flask_socketio import emit, join_room, rooms
from iris import app, models, db, socketio

COURSE_ID = 1


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/student')
def student():
    return redirect(url_for('student_feedback', course=1))


@app.route('/student/<course>')
def student_feedback(course):
    # TODO: Get course ID from database, course name = course
    course_id = COURSE_ID
    l_session = get_lecture_session(course_id)
    counts = dict()
    actions = app.config['BUTTON_ACTIONS']
    for action in actions:
        s_feedback = get_session_feedback(l_session.session_id, action[0])
        counts[action[0]] = s_feedback.count
    return render_template('chat.html', course_id=course_id, counts=counts, actions=actions)


@app.route('/lecturer')
def lecturer():
    return redirect(url_for('session_control'))


@app.route('/lecturer/session')
def session_control():
    return render_template('lecturer_session.html')


@socketio.on('student_send')
def handle_student_send(message):
    course_id = message['course_id']
    if course_id not in rooms():
        return
    l_session = get_lecture_session(course_id)
    if l_session.active:
        action = message['button']
        s_feedback = get_session_feedback(l_session.session_id, action)
        s_feedback.count += 1
        db.session.add(s_feedback)
        db.session.commit()
        emit('lecturer_recv', {'button': [action, s_feedback.count]}, room=course_id)


@socketio.on('lecturer_send')
def handle_lecturer_send(message):
    course_id = message['course_id']
    if course_id not in rooms():
        return
    l_session = get_lecture_session(course_id)
    new_state = message['session_control']
    if new_state == 'start' and not l_session.active:
        old_feedbacks = models.SessionFeedback.query.filter_by(session_id=l_session.session_id)
        for feedback in old_feedbacks.all():
            emit('lecturer_recv', {'button': [feedback.action_name, 0]}, room=course_id)
            db.session.delete(feedback)
        db.session.commit()
        l_session.active = True
    elif new_state == 'stop':
        l_session.active = False
    db.session.add(l_session)
    db.session.commit()


@socketio.on('join')
def client_connect(message):
    join_room(message['course_id'])


def get_lecture_session(course_id):
    return get_model_or_create(models.LectureSession, (course_id, ))


def get_session_feedback(session_id, action_name):
    return get_model_or_create(models.SessionFeedback, (session_id, action_name))


def get_model_or_create(model, parameters):
    retrieved_model = model.query.get(parameters)
    if retrieved_model is None:
        retrieved_model = model(*parameters)
        db.session.add(retrieved_model)
        db.session.commit()
    return retrieved_model
