from flask import render_template, redirect, url_for
from flask_socketio import emit, join_room, rooms
from flask_security import login_required, current_user
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
    course_id = get_course_id(course)
    l_session = get_lecture_session(course_id)
    actions = app.config['BUTTON_ACTIONS']
    all_questions = list(reversed(models.Questions.query.all()))
    return render_template('student_session.html',
                           course_id=course_id,
                           actions=actions,
                           active=l_session.active,
                           questions=all_questions)


@app.route('/lecturer')
@login_required
def lecturer():
    return redirect(url_for('session_control', course=1))


@app.route('/lecturer/<course>/session')
@login_required
def session_control(course):
    course_id = get_course_id(course)
    l_session = get_lecture_session(course_id)
    counts = dict()
    actions = app.config['BUTTON_ACTIONS']
    all_questions = list(reversed(models.Questions.query.all()))
    for action in actions:
        s_feedback = get_session_feedback(l_session.session_id, action[0])
        counts[action[0]] = s_feedback.count
    return render_template('lecturer_session.html',
                           course_id=course_id,
                           counts=counts,
                           actions=actions,
                           active=l_session.active,
                           questions=all_questions)


def handle_question(message, l_session, course_id):
    new_question = str(message['question'])
    s_question = models.Questions(l_session.session_id, new_question)
    db.session.add(s_question)
    emit('student_recv', message, room=course_id)
    emit('lecturer_recv', message, room=course_id)


def handle_feedback(message, l_session, course_id):
    action = message['action']
    s_feedback = get_session_feedback(l_session.session_id, action)
    s_feedback.count += 1
    db.session.add(s_feedback)
    emit('lecturer_recv', {'action': [action, s_feedback.count]}, room=course_id)


@socketio.on('student_send')
def handle_student_send(message):
    course_id = message['course_id']
    if course_id not in rooms():
        return
    l_session = get_lecture_session(course_id)
    if l_session.active:
        print(message)
        if 'action' in message:
            handle_feedback(message, l_session, course_id)
        elif 'question' in message:
            handle_question(message, l_session, course_id)
        db.session.commit()


@socketio.on('lecturer_send')
def handle_lecturer_send(message):
    if not current_user.is_authenticated:
        return
    course_id = message['course_id']
    if course_id not in rooms():
        return
    l_session = get_lecture_session(course_id)
    new_state = message['session_control']
    if new_state == 'start' and not l_session.active:
        old_feedbacks = models.SessionFeedback.query.filter_by(session_id=l_session.session_id)
        models.Questions.query.delete()
        emit('student_recv', {'command': "deleteQuestions"}, room=course_id)
        emit('lecturer_recv', {'command': "deleteQuestions"}, room=course_id)
        for feedback in old_feedbacks.all():
            emit('lecturer_recv', {'action': [feedback.action_name, 0]}, room=course_id)
            db.session.delete(feedback)
        db.session.commit()
        l_session.active = True
    elif new_state == 'stop':
        l_session.active = False
    emit('lecturer_recv', {'active': l_session.active}, room=course_id)
    emit('student_recv', {'active': l_session.active}, room=course_id)
    db.session.add(l_session)
    db.session.commit()


@socketio.on('join')
def client_connect(message):
    join_room(message['course_id'])


def get_course_id(course_name):
    # TODO: get correct course_name
    return COURSE_ID


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
