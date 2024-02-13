import logging

from sqlalchemy.exc import OperationalError

from wxcloudrun import db
from wxcloudrun.user.model import User  # 假设Users模型已经定义

# 初始化日志
logger = logging.getLogger('log')


def query_userbyid(uid):
    """
    根据UID查询用户实体
    :param uid: 用户的UID
    :return: 用户实体
    """
    try:
        return User.query.filter(User.uid == uid).first()
    except OperationalError as e:
        logger.info("query_userbyid errorMsg= {} ".format(e))
        return None


def delete_userbyid(uid):
    """
    根据UID删除用户实体
    :param uid: 用户的UID
    """
    try:
        user = User.query.get(uid)
        if user is None:
            return
     
        db.session.commit()
    except OperationalError as e:
        logger.info("delete_userbyid errorMsg= {} ".format(e))


def insert_user(user):
    """
    插入一个用户实体
    :param user: Users实体
    """
    try:
        db.session.add(user)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_user errorMsg= {} ".format(e))


def update_userbyid(user):
    """
    根据UID更新用户的值
    :param user: 用户实体
    """
    try:
        user_in_db = query_userbyid(user.uid)
        if user_in_db is None:
            return
        # 更新字段
        user_in_db.username = user.username
        user_in_db.status = user.status
        user_in_db.userType = user.userType
        user_in_db.password = user.password
        user_in_db.email = user.email
        user_in_db.phone = user.phone
        user_in_db.createdAt = user.createdAt
        user_in_db.updatedAt = user.updatedAt
        db.session.flush()
        db.session.commit()
    except OperationalError as e:
        logger.info("update_userbyid errorMsg= {} ".format(e))
