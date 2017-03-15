from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_debugtoolbar import DebugToolbarExtension
from flask_security import SQLAlchemyUserDatastore, Security

app = Flask(__name__)
app.config.from_object('config')
socketio = SocketIO(app, async_mode='eventlet')
db = SQLAlchemy(app)
toolbar = DebugToolbarExtension(app)

from iris import views, models  # noqa

user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)
