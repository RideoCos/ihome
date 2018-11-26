import os

from flask import render_template, request, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import re

from utils.functions import image_code, is_graph, is_name, is_card
from utils.models import db, User
from utils.settings import UPLOAD_DIR
from utils.status_code import *
from . import user_blue

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@user_blue.route('/create_db/')
def create_db():
    db.create_all()
    return 'OK'


@user_blue.route('/login/')
def login():
    if request.method == 'GET':
        return render_template('login.html')


@user_blue.route('/login_info/', methods=['POST'])
def login_info():
    if request.method == 'POST':
        mobile = request.form.get('phone')
        password = request.form.get('pwd')
        user = User.query.filter(User.phone == mobile).first()
        if user:
            if user.check_pwd(password):
                login_user(user)
                return jsonify({'code': OK})
            else:
                return jsonify({'code': USER_LOGIN_PWD_ERROR})
        else:
            return jsonify({'code': USER_LOGIN_PHONE_EXIETS})


@user_blue.route('/register/')
def register():
    if request.method == 'GET':
        return render_template('register.html')


@user_blue.route('/image_code/')
def register_image_code():
    if request.method == 'GET':
        i_code = image_code()
        session['image_code'] = i_code
        return jsonify({"code": OK, "image_code": i_code})


@user_blue.route('/register_info/', methods=['POST'])
def register_info():
    if request.method == 'POST':
        image_code = session.get('image_code')
        i_code = request.form.get('i_code')
        if image_code == i_code:
            mobile = request.form.get('mobile')
            password = request.form.get('password')
            user = User.query.filter(User.phone == mobile).first()
            if user:
                return jsonify({'code': USER_REGISTER_NOT_PHONE})
            if not re.match(r'(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$', mobile):
                return jsonify({'code': USER_REGISTER_PHONE_RE})
            new_user = User()
            new_user.phone = mobile
            new_user.password = password
            new_user.add_update()
            return jsonify({'code': OK})
        else:
            return jsonify({'code': USER_REGISTER_IMAGE_CODE})


@user_blue.route('/my/')
@login_required
def my():
    if request.method == 'GET':
        return render_template('my.html')


@user_blue.route('/my_info/')
@login_required
def my_info():
    if request.method == 'GET':
        info = current_user.to_basic_dict()
        info["code"] = OK
        return jsonify(info)


@user_blue.route('/logout/')
@login_required
def logout():
    if request.method == 'GET':
        logout_user()
        session.clear()
        return jsonify({'code': OK})


@user_blue.route('/profile/')
@login_required
def profile():
    if request.method == 'GET':
        return render_template('profile.html')


@user_blue.route('/profile_info/', methods=['POST'])
@login_required
def profile_info():
    if request.method == 'POST':
        avatar = request.files.get('avatar')
        name = request.form.get('name')
        if avatar:
            if is_graph(avatar.filename):
                file_path = os.path.join(UPLOAD_DIR, avatar.filename)
                avatar.save(file_path)
                user = current_user
                user.avatar = os.path.join('upload', avatar.filename)
                db.session.add(user)
                db.session.commit()
                return jsonify({'code': OK})
            else:
                return jsonify({'code': IMAGE_FORMAT_ERROR})
        if name:
            user = User.query.filter_by(name=name).first()
            if user:
                return jsonify({'code': USER_NAME_EXIETS})
            else:
                user = current_user
                user.name = name
                user.add_update()
                return jsonify({"code": OK})


@user_blue.route("/auth/")
@login_required
def auth():
    if request.method == 'GET':
        return render_template('auth.html')


@user_blue.route('/auth_info/', methods=['POST'])
@login_required
def auth_info():
    if request.method == 'POST':
        re_name = request.form.get('real_name')
        card = request.form.get('id_card')
        if all([re_name, card]):
            if not is_name(re_name):
                return jsonify({"code": USER_NAME_FORMAT_ERROR})
            if not is_card(card):
                return jsonify({"code": USER_AUTH_CID_ERROR})
            user = current_user
            user.id_name = re_name
            user.id_card = card
            user.add_update()
            return jsonify({"code": OK})
        else:
            return jsonify({"code": NO})


@user_blue.route('/auth_success/')
@login_required
def auth_success():
    if request.method == 'GET':
        user = current_user
        info = user.to_auth_dict()
        if not all([info["id_card"], info["id_name"]]):
            info["code"] = NO
        else:
            info["code"] = OK
        return jsonify(info)


