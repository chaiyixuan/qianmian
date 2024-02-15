from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Order(db.Model):
    __tablename__ = 'Order'

    orderid = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    uid = db.Column(db.String(50), db.ForeignKey('User.uid'), nullable=False)
    orderAmount = db.Column(db.Float, nullable=False)  # 支付金额
    paymentMethod = db.Column(db.String(50), nullable=False)  # 支付方式
    orderDesc = db.Column(db.String(50))  # 订单详情说明
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())

    # 关联User表
    user = db.relationship('User', backref=db.backref('order', lazy=True))

    def __repr__(self):
        return '<Order %r>' % self.orderid
