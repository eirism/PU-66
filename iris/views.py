"""Module for the views and handlers for socketIO."""

from flask import render_template
from flask_security import login_required, current_user
from flask_socketio import emit, join_room, rooms
import indicoio

from iris import app, models, db, socketio, user_datastore, similarity


@app.route('/')
@app.route('/index')
def index():
    """The main entry point."""
    all_courses = models.Course.query.all()
    return render_template('index.html', courses=all_courses)


@app.route('/student/<course>')
def student_feedback(course):
    """

    The student view of a feedback session.

    Retrieves the available button actions,
    the current questions and the lecture's status.

    """
    course_id = get_course_id(course)
    l_session = get_lecture_session(course_id)
    actions = app.config['BUTTON_ACTIONS']
    grouped_questions = get_and_group_questions(l_session.session_id)
    return render_template('student_session.html',
                           course_id=course_id,
                           actions=actions,
                           active=l_session.active,
                           questions=grouped_questions,
                           course_code=course)


@app.route('/lecturer')
@login_required
def lecturer():
    """

    The lecturer main page.

    Where lecturers can see their courses, add new ones,
    join existing ones and start a feedback session.

    """
    all_courses = models.Course.query.all()
    existing_courses = [course for course in all_courses if course not in current_user.roles]
    return render_template('lecturer.html', my_courses=current_user.roles, courses=all_courses,
                           existing_courses=existing_courses)


@app.route('/lecturer/<course>/session')
@login_required
def session_control(course):
    """The lecturer view of a feedback session."""
    course_id = get_course_id(course)
    l_session = get_lecture_session(course_id)
    counts = dict()
    actions = app.config['BUTTON_ACTIONS']
    grouped_questions = get_and_group_questions(l_session.session_id)
    for action in actions:
        s_feedback = get_session_feedback(l_session.session_id, action[0])
        counts[action[0]] = s_feedback.count
    return render_template('lecturer_session.html',
                           course_id=course_id,
                           counts=counts,
                           actions=actions,
                           active=l_session.active,
                           questions=grouped_questions,
                           course_code=course)


def handle_question(message, l_session, course_id):
    """Create a new question, saves it and push it to the correct clients."""
    new_question = str(message['question'])
    all_questions = models.Questions.query.filter_by(session_id=l_session.session_id).all()
    questions = list()
    max_group = -1
    similar_questions = list()
    for q in all_questions:
        questions.append(q.question)
        if q.group > max_group:
            max_group = q.group
    # Needs atleast two existing questions to compare for reasons unknown
    if len(questions) < 2:
        group = max_group
    else:
        try:
            similar_questions = similarity.similarity(questions, new_question, 0.73)
            print("similar questions found: ", similar_questions)
        except Exception as e:
            print(e)
    if similar_questions:
        # Get group
        for q in all_questions:
            if similar_questions[0] == q.question:
                group = q.group
    else:
        group = max_group + 1
    keyword = extract_keyword(new_question)
    course_responses = models.Response.query.filter_by(course_id=course_id)
    matching_response = course_responses.filter_by(keyword=keyword).first()
    if matching_response is not None:
        q_response = matching_response.response
    else:
        q_response = None
    s_question = models.Questions(l_session.session_id, new_question, group,
                                  response=q_response)
    db.session.add(s_question)
    response = {'question': [new_question, group, q_response]}
    emit('student_recv', response, room=course_id)
    emit('lecturer_recv', response, room=course_id)


def handle_feedback(message, l_session, course_id):
    """Increment a feedback's count and push it to the lecturer(s)."""
    action = message['action']
    s_feedback = get_session_feedback(l_session.session_id, action)
    s_feedback.count += 1
    db.session.add(s_feedback)
    emit('lecturer_recv', {'action': [action, s_feedback.count]}, room=course_id)


@socketio.on('lecturer_keyword_new')
def handle_new_keyword(message):
    """

    Receive json from lecturer,
    add keywords and associated response to the database.
    Push updates

    """
    course_id = message['course_id']
    if course_id not in rooms():
        return
    keywords = message['keywords']
    response = message['response']
    print(message)
    for keyword in keywords.split(','):
        keyword = keyword.strip()
        new_keyword = models.Response(keyword, course_id, response)
        db.session.add(new_keyword)
    l_session = get_lecture_session(course_id)
    questions = get_and_group_questions(l_session.session_id)
    for group in questions:
        for question in questions[group]:
            old_question = get_question(l_session.session_id, question.question)
            keyword = extract_keyword(old_question.question)
            course_responses = models.Response.query.filter_by(course_id=course_id)
            matching_response = course_responses.filter_by(keyword=keyword).first()
            if matching_response is not None:
                q_response = matching_response.response
            else:
                q_response = None
            old_question.response = q_response
            db.session.add(old_question)
    db.session.commit()
    emit('new_response', {'reload': True}, room=course_id)


@socketio.on('student_send')
def handle_student_send(message):
    """Receive json from students and perform the action associated with the content."""
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
    """

    Handle incoming json from lecturers.

    Receive json from lecturers, starting and stopping the session
    according to the messages content.

    If session is stopped and then started, the associated feedback
    are deleted.

    """
    if not current_user.is_authenticated:
        return
    course_id = message['course_id']
    if course_id not in rooms():
        return
    l_session = get_lecture_session(course_id)
    new_state = message['session_control']
    if new_state == 'start' and not l_session.active:
        old_feedbacks = models.SessionFeedback.query.filter_by(session_id=l_session.session_id)
        models.Questions.query.filter_by(session_id=l_session.session_id).delete()
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


@socketio.on('lecturer_course_new_send')
def handle_lecturer_course_new(message):
    """

    Receives socket emitted from lecturer page when creating and subsequently adding a new
    course

    Emits a socket back with the recently added data for "instant" display on the page

    """
    if not current_user.is_authenticated:
        return
    code = message['code']
    name = message['name']
    # TODO: fix unique constraint in new migration
    if models.Course.query.filter_by(code=code).count() > 0:
        return
    new_course = user_datastore.create_role(code=code, name=name)
    user_datastore.add_role_to_user(current_user, new_course)
    db.session.commit()

    emit('lecturer_course_new_recv', {
        'code': code,
        'name': name
    })


@socketio.on('lecturer_course_existing_send')
def handle_lecturer_course_existing(message):
    """

    Receives socket emitted from lecturer page when adding an existing course to "my courses"

    Emits a socket back with the recently added data for "instant" display on the page

    """
    print('im in')
    if not current_user.is_authenticated:
        return
    code = message['code']
    name = message['name']
    existing_course = models.Course.query.filter_by(code=code).first_or_404()
    if existing_course in current_user.roles:
        return
    user_datastore.add_role_to_user(current_user, existing_course)
    db.session.commit()

    emit('lecturer_course_existing_recv', {
        'code': code,
        'name': name
    })


@socketio.on('join')
def client_connect(message):
    """Join students and lecturers to the room matching the course ID."""
    join_room(message['course_id'])


def get_course_id(course_name):
    """Return the course ID for the course with the given name."""
    return models.Course.query.filter_by(code=course_name).first_or_404().id


def get_lecture_session(course_id):
    """Retrieve the current session for the given course ID."""
    return get_model_or_create(models.LectureSession, {'course_id': course_id})


def get_question(session_id, question):
    return get_model_or_create(models.Questions, {'session_id': session_id,
                                                  'question': question})


def get_session_feedback(session_id, action_name):
    """

    Retrieve the the feedback with name matching action_name.

    A new one will be created if none matches.

    """
    return get_model_or_create(models.SessionFeedback, {'session_id': session_id,
                                                        'action_name': action_name})


def get_model_or_create(model, parameters):
    """

    Retrieve a database object (of type model) matching the parameters dict.

    The dict is unpacked when filtering.
    If no matching object is found, a new one is created.

    """
    models_matching = model.query.filter_by(**parameters)
    if models_matching.count() > 1:
        raise RuntimeError('More than one row matched query.')
    else:
        retrieved_model = models_matching.first()
    if retrieved_model is None:
        retrieved_model = model(**parameters)
        db.session.add(retrieved_model)
        db.session.commit()
    return retrieved_model


def get_and_group_questions(session_id):
    """

    Return a grouped dict of questions.

    The key are the group id and the value a list of the questions.

    """
    all_questions = reversed(models.Questions.query.filter_by(session_id=session_id).all())
    grouped_questions = dict()
    for question in all_questions:
        grouped_questions.setdefault(question.group, list()).append(question)
    return grouped_questions


def extract_keyword(text):
    """

    Ask INDICO for the keyword in text.

    Returns the most important word in text,
    or None if there is none.
    Calls .lower() on the word.

    """
    response = indicoio.keywords(text, version=2, top_n=1)
    words = list(response.keys())
    if len(words) == 1:
        word = list(response.keys())[0].lower()
    else:
        word = None
    return word
