import logging

from sqlalchemy.exc import OperationalError

from wxcloudrun import db
from wxcloudrun.member.model import Member  # 假设Member模型已经定义

# 初始化日志
logger = logging.getLogger('log')


def query_memberbyid(member_id):
    """
    根据会员ID查询会员实体
    :param member_id: 会员的ID
    :return: 会员实体
    """
    try:
        return Member.query.filter(Member.memberId == member_id).first()
    except OperationalError as e:
        logger.info("query_memberbyid errorMsg= {} ".format(e))
        return None


def delete_memberbyid(member_id):
    """
    根据会员ID删除会员实体
    :param member_id: 会员的ID
    """
    try:
        member = Member.query.get(member_id)
        if member is None:
            return
        
        db.session.delete(member)
        db.session.commit()
    except OperationalError as e:
        logger.info("delete_memberbyid errorMsg= {} ".format(e))


def insert_member(member):
    """
    插入一个会员实体
    :param member: Member实体
    """
    try:
        db.session.add(member)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_member errorMsg= {} ".format(e))


def update_memberbyid(member):
    """
    根据会员ID更新会员的值
    :param member: 会员实体
    """
    try:
        member_in_db = query_memberbyid(member.memberId)
        if member_in_db is None:
            return
        # 更新字段
        member_in_db.uid = member.uid
        member_in_db.memberStart = member.memberStart
        member_in_db.memberEnd = member.memberEnd
        member_in_db.memberStatus = member.memberStatus
        member_in_db.createdAt = member.createdAt
        member_in_db.updatedAt = member.updatedAt
        db.session.flush()
        db.session.commit()
    except OperationalError as e:
        logger.info("update_memberbyid errorMsg= {} ".format(e))
