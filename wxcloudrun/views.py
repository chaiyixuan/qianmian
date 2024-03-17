from datetime import datetime, timedelta
from flask import render_template, request
from run import app
from wxcloudrun.dao import (
    delete_counterbyid,
    query_counterbyid,
    insert_counter,
    update_counterbyid,
)
import logging
from wxcloudrun.user.dao import (
    query_userbyid,
    delete_userbyid,
    insert_user,
    update_userbyid,
)
from wxcloudrun.user.model import User
from wxcloudrun.member.dao import insert_member, update_memberbyid, query_memberbyid
from wxcloudrun.member.model import Member
from wxcloudrun.knowlagebase.dao import (
    query_knowlage_base_by_uid,
    query_knowlage_base_by_kid,
)
from wxcloudrun.knowlagebase.model import KnowlageBase
from wxcloudrun.order.dao import update_orderbyid, insert_order, query_orderbyid
from wxcloudrun.order.model import Order
from wxcloudrun.model import Counters
import requests


# from wxcloudrun.local_config import Config

from wxcloudrun.response import (
    make_succ_empty_response,
    make_succ_response,
    make_err_response,
)
from wxcloudrun.util import generate_uid
import os

# 初始化日志
logger = logging.getLogger("log")

is_debug = True


if is_debug:
    # config = Config()
    # APPID = config.APPID
    # SECRET = config.SECRET
    APPID = ""
    SECRET = ""
    print(APPID)
    print(SECRET)

    # WEIXIN_URL = "wxcloud-localdebug-proxy-91759-7-1323921410.sh.run.tcloudbase.com"
    WEIXIN_URL = "api.weixin.qq.com"
else:
    APPID = os.environ.get("WEIXIN_APPID")
    SECRET = os.environ.get("WEIXIN_SECRET")
    WEIXIN_URL = "api.weixin.qq.com"


@app.route("/")
def index():
    """
    :return: 返回index页面
    """
    return render_template("index.html")



def register(uid):
    """
    注册用户
    :return:
    """

    # 获取请求体参数
    params = request.get_json()

    # username = params["username"]

    uid = generate_uid()
    user = User()
    # user.username = username
    user.uid = uid
    user.created_at = datetime.now()
    user.updated_at = datetime.now()
    try:
        insert_user(user)
        return uid
        # return make_succ_response(uid)
    except Exception as e:
        return ""
        # return make_err_response(e)


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

@app.route("/api/user/login", methods=["POST"])
def login():
    # 获取请求体参数s
   
    openID = request.headers.get('x-wx-openid')
    # unionID认证后才会有
    # unionID = request.headers.get('x-wx-unionid')
    if len(openID)>0:
        # 查询是否注册,没有就新增，有就返回
        user = query_userbyid(openID)
        if user:
            return make_succ_response({"uid": openID})
        else:
            uid = register(openID)
            return make_succ_response({"uid": uid})
    else:
        return make_err_response("没有获得用户id")
    

    

@app.route("/api/user/get_union_id", methods=["POST"])
def get_union_id():
    # 获取请求体参数
    params = request.get_json()
    JSCODE = params["code"]
    # 构造请求的URL
    url = "https://" + WEIXIN_URL + "/sns/jscode2session"
    params = {
        "appid": APPID,
        "secret": SECRET,
        "js_code": JSCODE,
        "grant_type": "authorization_code",
    }
    logger.error("get_union_id")

    # 发送GET请求
    response = requests.get(url, params=params)

    # 检查响应状态码
    # if response.status_code == 200:
    # 请求成功，处理响应数据
    logger.error(response)
    data = response.json()
    if data["errcode"] == 0:
        return make_succ_response(
            {
                "unionid": data["unionid"],
                "session_key": data["session_key"],
                "errcode": data["errcode"],
            }
        )
    else:
        return make_err_response({"errcode": data["errcode"], "errmsg": data["errmsg"]})


@app.route("/api/user/getopenid", methods=["POST"])
def get_openid():
    # 获取请求体参数
    params = request.get_json()
    JSCODE = params["code"]
    # 构造请求的URL
    url = "https://" + WEIXIN_URL + "/sns/jscode2session"
    params = {
        "appid": APPID,
        "secret": SECRET,
        "js_code": JSCODE,
        "grant_type": "authorization_code",
    }
    logger.error("get_openid")

    # 发送GET请求
    # response = requests.get(url, params=params)

    # 检查响应状态码
    # if response.status_code == 200:
    # 请求成功，处理响应数据

    # data = response.json()

    # openid = data.openid
    openid = "123ccx2"
    user = query_userbyid(openid)
    # 我们的表里面已经有该用户
    if user:
        logger.error("login success")
    else:
        # 没有用户就注册
        user = User()
        user.username = "username0302"
        user.uid = openid
        insert_user(user)
        # TODO: 是否要插入member表

        # {
        # "openid":"xxxxxx",
        # "session_key":"xxxxx",
        # "unionid":"xxxxx",
        # "errcode":0,
        # "errmsg":"xxxxx"
        # }

    return make_succ_response(str(openid))
    # else:
    #     logger.error("error{}".format(url))
    #     return make_err_response(response.status_code)


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


@app.route("/api/knowlage/get_knowlages", methods=["GET"])
def get_knowlages():
    """
    :return: 根据uid查文章
    """
    try:
        uid = request.args.get("uid", default="002")

        knowlage_bases = query_knowlage_base_by_uid(uid)
        # knowlage_bases = queryToDict(knowlage_bases)
        kid_list = [{"kid": entity.kid} for entity in knowlage_bases]
    except Exception as e:
        return make_err_response(str(e))
    # logger.error("knowlage_bases{}".format(kid_list))
    return make_succ_response(kid_list)


@app.route("/api/knowlage/get_knowlage_detail", methods=["POST"])
def get_knowlage_by_kid():
    """
    :return: 根据uid查文章
    """
    try:
        params = request.get_json()
        kid = params["kid"]
        knowlage_base = query_knowlage_base_by_kid(kid)
        kb_obj = {"kid": knowlage_base.kid, "content": knowlage_base.content}
    except Exception as e:
        return make_err_response(str(e))

    # print("knowlage_base",knowlage_base)
    # logger.error("knowlage_base{}".format(knowlage_base.to_dict()))
    return make_succ_response(kb_obj)
