from iris import db


class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))

    def __repr__(self):
        return '<Text {:r}>'.format(self.content)
