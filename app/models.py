from . import db, login
from flask_login import UserMixin
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    autobase = db.relationship('Autobase', backref='owner', lazy='dynamic')

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Autobase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(64), index=True, unique=True)
    status = db.Column(db.Boolean, default=False)
    consumer = db.Column(db.String(80))
    secret = db.Column(db.String(80))
    CONSUMER_KEY = db.Column(db.String(80))
    CONSUMER_SECRET = db.Column(db.String(80))
    ACCESS_KEY = db.Column(db.String(80))
    ACCESS_SECRET = db.Column(db.String(80))
    ENV_NAME = db.Column(db.String(80))

    def __repr__(self) -> str:
        return f'<Autobase {self.name}>'

