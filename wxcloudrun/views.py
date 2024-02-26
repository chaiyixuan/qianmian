from datetime import datetime, timedelta
from flask import render_template, request
from run import app
from wxcloudrun.dao import (
    delete_counterbyid,
    query_counterbyid,
    insert_counter,
    update_counterbyid,
)
from wxcloudrun.user.dao import query_userbyid, delete_userbyid, insert_user, update_userbyid
from wxcloudrun.user.model import User
from wxcloudrun.member.dao import insert_member, update_memberbyid, query_memberbyid
from wxcloudrun.member.model import Member
from wxcloudrun.order.dao import update_orderbyid, insert_order, query_orderbyid
from wxcloudrun.order.model import Order
from wxcloudrun.model import Counters
import requests


from wxcloudrun.response import (
    make_succ_empty_response,
    make_succ_response,
    make_err_response,
)
from wxcloudrun.util import generate_uid
import os

APPID = os.environ.get("WEIXIN_APPID")
SECRET = os.environ.get("WEIXIN_SECRET")


@app.route("/")
def index():
    """
    :return: 返回index页面
    """
    return render_template("index.html")


@app.route("/api/user/register", methods=["POST"])
def register():
    """
    注册用户
    :return:
    """

    # 获取请求体参数
    params = request.get_json()

    username = params["username"]

    uid = generate_uid()
    user = User()
    user.username = username
    user.uid = uid
    user.created_at = datetime.now()
    user.updated_at = datetime.now()
    try:
        insert_user(user)
        return make_succ_response(uid)
    except Exception as e:
        return make_err_response(e)


app.route("/api/member/buy_membership", methods=["POST"])


def buy_membership():
    """
    用户购买会员
    :return:
    """

    # 获取请求体参数
    params = request.get_json()

    uid = params["uid"]
    orderDesc = params["orderDesc"]
    member_type = params.get("memberType", 0)  # 1为普通会员，2为超级会员

    # 查询用户是否存在，以及是否已经是会员
    # 这里是查询数据库的逻辑，根据实际情况实现
    user = query_userbyid(uid)
    if not user:
        return make_err_response("用户不存在")

    # 用户已经是会员，检查会员类型和有效期
    if user.member.memberType != 0:
        # 2会员续费1会员
        if user.member.member_type > member_type:
            return make_err_response("已经是更高级别的会员")
        # 同级别会员增加时间
        elif user.member.member_type == member_type:  # 续费
            user.member.memberEnd = user.member.memberEnd + timedelta(days=90)
            # 这里是处理支付逻辑，根据实际情况实现
            # 需要更新会员类型和有效期
            insert_member(user.member)
        # 低级别会员购买高级别 可以将剩余的VIP会员时间按比例计算其价值，然后从SVIP会员费用中扣除
        elif user.member.member_type < member_type:
            pass
    # 非会员
    else:
        user.member.memberEnd = user.member.memberEnd + timedelta(days=90)
        # 用户不是会员，创建会员记录
        insert_member(user.member)

    return make_succ_response("购买会员成功")


@app.route("/api/user/getopenid", methods=["POST"])
def get_openid():
    # 获取请求体参数
    params = request.get_json()
    JSCODE = params["code"]
    # 构造请求的URL
    url = "https://api.weixin.qq.com/sns/jscode2session"
    params = {
        "appid": APPID,
        "secret": SECRET,
        "js_code": JSCODE,
        "grant_type": "authorization_code",
    }

    # 发送GET请求
    response = requests.get(url, params=params)

    # 检查响应状态码
    if response.status_code == 200:
        # 请求成功，处理响应数据
        data = response.json()
        # {
        # "openid":"xxxxxx",
        # "session_key":"xxxxx",
        # "unionid":"xxxxx",
        # "errcode":0,
        # "errmsg":"xxxxx"
        # }

        return make_succ_response(data)
    else:
        return make_err_response("")


@app.route("/api/count", methods=["POST"])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if "action" not in params:
        return make_err_response("缺少action参数")

    # 按照不同的action的值，进行不同的操作
    action = params["action"]

    # 执行自增操作
    if action == "inc":
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == "clear":
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response("action参数错误")


@app.route("/api/count", methods=["GET"])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return (
        make_succ_response(0) if counter is None else make_succ_response(counter.count)
    )
