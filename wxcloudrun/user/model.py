from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'

    uid = db.Column(db.String(50), unique=True, nullable=False,primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.Integer, default=False)  # 禁用与否，默认不禁用
    userType = db.Column(db.Integer, default=False)  # 是否管理员，默认不是管理员
    password = db.Column('password', db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())

    # @property
    # def password(self):
    #     raise AttributeError('password is not a readable attribute')

    # @password.setter
    # def password(self, password):
    #     self._password = generate_password_hash(password)

    # def verify_password(self, password):
    #     return check_password_hash(self._password, password)

    # def __repr__(self):
    #     return '<User %r>' % self.username
