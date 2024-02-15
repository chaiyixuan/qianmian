from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Member(db.Model):
    __tablename__ = 'Member'

    memberId = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    uid = db.Column(db.String(50), db.ForeignKey('User.uid'), nullable=False)
    memberStart = db.Column(db.TIMESTAMP, nullable=False)
    memberEnd = db.Column(db.TIMESTAMP, nullable=False)
    memberStatus = db.Column(db.Integer, default=0)  # 0非会员 1会员 2超级会员
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    # 关联User表
    user = db.relationship('User', backref=db.backref('member', lazy=True))

    def __repr__(self):
        return '<Member %r>' % self.memberId
