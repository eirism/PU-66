from flask import redirect
from flask import render_template
from flask import url_for
from flask_socketio import emit
from iris import app, models, db, socketio


@app.route('/')
@app.route('/index')
def index():
    return render_template('startpage.html')


@app.route('/student')
def student():
    return 'Hello, student'


@app.route('/lecturer')
def lecturer():
    return redirect(url_for('session_control'))


@app.route('/lecturer/session')
def session_control():
    return render_template('lecturer_session.html')




@socketio.on('my_event')
def handle_text(message):
    new_text = models.Text(content=message)
    db.session.add(new_text)
    db.session.commit()
    emit('brd_text', message, broadcast=True)


@socketio.on('connect')
def client_connect():
    print('Client connected')
