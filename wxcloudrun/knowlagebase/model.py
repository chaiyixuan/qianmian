from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class KnowlageBase(db.Model):
    __tablename__ = 'KnowlageBase'

    kid = db.Column(db.String(50), unique=True, nullable=False,primary_key=True)
    content = db.Column(db.Text,  nullable=False)
    uid = db.Column(db.String(50), db.ForeignKey('User.uid'), nullable=False)
    title = db.Column('title', db.String(150), nullable=False)
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    # def to_dict(self):
    #     # 创建一个新字典来保存对象的数据
    #     knowledge_dict = {}
    #     for column in self.__table__.columns:
    #         # 检查列是否是日期类型
    #         if isinstance(column.type, db.DateTime):
    #             # 如果是日期类型，格式化为 'YYYY年MM月DD日' 格式
    #             knowledge_dict[column.name] = self.__dict__[column.name].starftime('%Y年%m月%d日')
    #         else:
    #             # 其他列直接添加到字典
    #             knowledge_dict[column.name] = self.__dict__[column.name]
        
    #     # # 删除不需要的字段，例如密码字段（如果存在）
    #     # del knowledge_dict['password_hash']  # 假设User模型中有password_hash字段

    #     return knowledge_dict