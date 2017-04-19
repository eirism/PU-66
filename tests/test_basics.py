def test_init(app, session, client, client_socketio):
    """Tests that the app is initialized correctly (no errors)"""
    pass


def check_status_code(client, endpoints, code):
    for endpoint in endpoints:
        rv = client.get(endpoint)
        assert rv.status_code == code


def test_200_routes(client):
    endpoints = ['/']
    check_status_code(client, endpoints, 200)


def test_200_logged_in_course(create_default_course, logged_in_user, client):
    endpoints = ['/lecturer/TDT4140/session', '/lecturer']
    check_status_code(client, endpoints, 200)


def test_200_course(create_default_course, client):
    endpoints = ['/student/TDT4140']
    check_status_code(client, endpoints, 200)


def test_socketio_join(client_socketio):
    client_socketio.emit('join', {'course_id': 1})


def test_create_course(logged_in_user, client_socketio):
    course_code = 'TDT4180'
    course_name = 'MMI'
    client_socketio.emit('lecturer_course_new_send',
                         {'code': course_code, 'name': course_name})
    response = client_socketio.get_received()[0]
    args = response['args'][0]
    assert args['code'] == course_code
    assert args['name'] == course_name


def test_join_course(create_default_course, logged_in_user, client_socketio):
    course = create_default_course
    client_socketio.emit('lecturer_course_existing_send',
                         {'code': course.code, 'name': course.name})
    response = client_socketio.get_received()[0]
    args = response['args'][0]
    assert args['code'] == course.code
    assert args['name'] == course.name


def test_socketio_room_not_joined(client_socketio):
    client_socketio.emit('student_send', {'course_id': 1, 'action': 'slow'})
    client_socketio.emit('lecturer_send', {'course_id': 1, 'session_control': 'start'})
    assert len(client_socketio.get_received()) == 0


def test_socketio_keywords(logged_in_user, client_socketio):
    pre_response = 'Objects are from OOP'
    client_socketio.emit('join', {'course_id': 1})
    client_socketio.emit('lecturer_send', {'course_id': 1, 'session_control': 'start'})
    client_socketio.emit('lecturer_keyword_new', {'course_id': 1,
                                                  'keywords': 'objects',
                                                  'response': pre_response})
    client_socketio.emit('student_send', {'course_id': 1, 'question': 'What are objects?'})
    response = client_socketio.get_received()[-1]['args'][0]['question'][2]
    assert pre_response == response


def get_question_group(response):
    return response['args'][0]['question'][1]


def test_socketio_send_student(logged_in_user, client_socketio):
    client_socketio.emit('join', {'course_id': 1})
    client_socketio.emit('lecturer_send', {'course_id': 1, 'session_control': 'start'})
    client_socketio.emit('student_send', {'course_id': 1, 'action': 'slow'})
    lecturer_response = client_socketio.get_received()[-1]
    assert lecturer_response['name'] == 'lecturer_recv'
    assert lecturer_response['args'][0] == {'action': ['slow', 1]}
    q1 = 'This is a long question.'
    q2 = 'Then how about this? Is it long enough?'
    q3 = 'How are you? I am fine.'
    client_socketio.emit('student_send', {'course_id': 1, 'question': q1})
    g1 = get_question_group(client_socketio.get_received()[-1])
    client_socketio.emit('student_send', {'course_id': 1, 'question': q2})
    g2 = get_question_group(client_socketio.get_received()[-1])
    client_socketio.emit('student_send', {'course_id': 1, 'question': q3})
    g3 = get_question_group(client_socketio.get_received()[-1])
    # Check that the previous questions aren't grouped together
    assert g1 != g2 and g2 != g3 and g1 != g3
