import jwt
from datetime import datetime, timezone, timedelta
from flask import current_app
from flask_login import UserMixin
from flask_security import RoleMixin

from test_flask_lesson import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='user', lazy=True)

    def __repr__(self):
        return f"Role('{self.name}')"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String, db.ForeignKey('role.name'), nullable=False, default='user')
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    def get_reset_token(self, expire_sec=1800):
        payload = {'user_id': self.id, 'exp': datetime.now(timezone.utc) + timedelta(seconds=expire_sec)}
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
        #serializer = Serializer(current_app.config['SECRET_KEY'], expire_sec)
        #return serializer.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token, leeway=timedelta(seconds=10)):
        # serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], leeway=leeway, algorithms=['HS256'])
            #user_id = serializer.loads(token)['user_id']
        except Exception:
            return None
        return User.query.get(data['user_id'])


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='title', lazy='dynamic')
    likes = db.relationship('Like', backref='title', lazy='dynamic')

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    username = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.text}', '{self.username}')"


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    username = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)

    def __repr__(self):
        return f"Like('{self.post_id}', '{self.username}')"

