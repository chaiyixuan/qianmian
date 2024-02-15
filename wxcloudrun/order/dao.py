import logging

from sqlalchemy.exc import OperationalError

from wxcloudrun import db
from wxcloudrun.order.model import Order  # 假设Order模型已经定义

# 初始化日志
logger = logging.getLogger('log')


def query_orderbyid(order_id):
    """
    根据订单ID查询订单实体
    :param order_id: 订单的ID
    :return: 订单实体
    """
    try:
        return Order.query.filter(Order.orderId == order_id).first()
    except OperationalError as e:
        logger.info("query_orderbyid errorMsg= {} ".format(e))
        return None


def delete_orderbyid(order_id):
    """
    根据订单ID删除订单实体
    :param order_id: 订单的ID
    """
    try:
        order = Order.query.get(order_id)
        if order is None:
            return
        
        db.session.delete(order)
        db.session.commit()
    except OperationalError as e:
        logger.info("delete_orderbyid errorMsg= {} ".format(e))


def insert_order(order):
    """
    插入一个订单实体
    :param order: Order实体
    """
    try:
        db.session.add(order)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_order errorMsg= {} ".format(e))


def update_orderbyid(order):
    """
    根据订单ID更新订单的值
    :param order: 订单实体
    """
    try:
        order_in_db = query_orderbyid(order.orderId)
        if order_in_db is None:
            return
        # 更新字段
        order_in_db.uid = order.uid
        order_in_db.orderAmount = order.orderAmount
        order_in_db.paymentMethod = order.paymentMethod
        order_in_db.orderDesc = order.orderDesc
        order_in_db.createdAt = order.createdAt
        order_in_db.updatedAt = order.updatedAt
        db.session.flush()
        db.session.commit()
    except OperationalError as e:
        logger.info("update_orderbyid errorMsg= {} ".format(e))
