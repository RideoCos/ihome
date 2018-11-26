
from utils.functions import get_mysql_url,get_redis_url

class Config():
    # session配置
    SESSION_TYPE = 'redis'
    SESSION_REDIS = get_redis_url()

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = get_mysql_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 密钥设置
    SECRET_KEY = 'secret_key'
