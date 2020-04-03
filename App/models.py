from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from App import app

db = SQLAlchemy(app)


class contactTable(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    msg_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    name = db.Column(db.String(80))
    email = db.Column(db.String(120))
    title = db.Column(db.String(256))
    message = db.Column(db.String(600000))

    def __repr__(self):
        return '<name {}> <email {}> <title {}> <message {}> <date {}>'.format(self.name, self.email,
                                                                               self.title, self.message,
                                                                               self.msg_date)
