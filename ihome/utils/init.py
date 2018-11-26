from flask import Flask
from flask_session import Session

from house import house_blue
from order import order_blue
from utils.models import db
from user.views import login_manager
from user import user_blue
from utils.config import Config
from utils.settings import STATIC_DIR, TEMPLATES_DIR


def init_ext(app):
    # 获取Session对象，并初始化app
    se = Session()
    se.init_app(app)
    # 绑定db和app
    db.init_app(app)
    # 绑定login_manager和app
    login_manager.login_view = 'user.login'
    login_manager.init_app(app)


def create_app():
    app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATES_DIR)
    # 数据库连接
    app.config.from_object(Config)
    # 注册蓝图
    app.register_blueprint(blueprint=user_blue, url_prefix='/user')
    app.register_blueprint(blueprint=house_blue, url_prefix='/house')
    app.register_blueprint(blueprint=order_blue, url_prefix='/order')
    # 初始化
    init_ext(app)
    return app
