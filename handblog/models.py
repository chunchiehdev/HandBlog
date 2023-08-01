from datetime import datetime
from flask import current_app
from handblog import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash ,check_password_hash



@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    #author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    
    # 外來鍵    
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

# 建立模型
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(120), nullable = False, unique = True)
    favorite_song = db.Column(db.String(120))
    about_author = db.Column(db.Text(), nullable = True)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)
    profile_pic = db.Column(db.String, nullable = True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    registered_on = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)

    posts = db.relationship('Posts', backref='poster')

    @property
    def password(self):
        raise AttributeError('Password Error！Unrecognizable！')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<name %r>' % self.name