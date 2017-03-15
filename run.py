from iris import app, socketio

socketio.run(app, host='0.0.0.0', port=app.config['PORT'], debug=app.config['DEBUG'])
