def test_init(app, session, client, client_socketio):
    """Tests that the app is initialized correctly (no errors)"""
    pass


def test_200_routes(client):
    endpoints = ['/', '/student/session']
    from sys import stderr
    for endpoint in endpoints:
        tmp_rv = client.get(endpoint)
        stderr.write(endpoint + '\n')
        assert tmp_rv.status_code == 200


def test_socketio_join(client_socketio):
    client_socketio.emit('join', {'course_id': 1})


def test_socketio_room_not_joined(client_socketio):
    client_socketio.emit('student_send', {'course_id': 1, 'action': 'slow'})
    client_socketio.emit('lecturer_send', {'course_id': 1, 'session_control': 'start'})
    assert len(client_socketio.get_received()) == 0


def test_socketio_send_student(client_socketio):
    client_socketio.emit('join', {'course_id': 1})
    client_socketio.emit('lecturer_send', {'course_id': 1, 'session_control': 'start'})
    client_socketio.emit('student_send', {'course_id': 1, 'action': 'slow'})
    lecturer_response = client_socketio.get_received()[-1]
    assert lecturer_response['name'] == 'lecturer_recv'
    assert lecturer_response['args'][0] == {'action': ['slow', 1]}
