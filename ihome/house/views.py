import os

from flask import request, render_template, jsonify, session
from flask_login import login_required, current_user
import datetime


from utils.functions import is_graph
from utils.models import db, Area, Facility, House, HouseImage
from utils.settings import UPLOAD_DIR
from utils.status_code import OK, IMAGE_FORMAT_ERROR, NO
from . import house_blue


# 区域数据
@house_blue.route('/create_data/')
def create_data():
    areas = ['北京市','天津市','上海市','重庆市','河北省','山西省',
             '辽宁省','吉林省','黑龙江省','江苏省','浙江省','安徽省',
             '福建省','江西省','山东省','河南省','湖北省','湖南省',
             '广东省','海南省','四川省','贵州省','云南省','陕西省',
             '甘肃省','青海省','台湾省','内蒙古自治区','广西壮族自治区',
             '西藏自治区','宁夏回族自治区','新疆维吾尔自治区','香港特别行政区','澳门特别行政区']
    now_time = datetime.datetime.now()
    update_time = datetime.datetime.now()
    add_list =[]
    for item in areas:
        info = Area()
        info.name = item
        info.create_time = now_time
        info.update_time = update_time
        add_list.append(info)
    db.session.add_all(add_list)
    db.session.commit()
    return 'success'


@house_blue.route('/my_house/')
@login_required
def my_house():
    if request.method == 'GET':
        return render_template('myhouse.html')


@house_blue.route('/my_house_info/')
@login_required
def my_house_info():
    houses = House.query.filter_by(user_id=current_user.id).all()
    data = []
    for house in houses:
        data.append(house.to_dict())
    return jsonify(data)


@house_blue.route('/my_house_auth/')
@login_required
def my_house_auth():
    if request.method == 'GET':
        user = current_user
        info = user.to_auth_dict()
        if not all([info["id_card"], info["id_name"]]):
            return jsonify({"code": NO})
        else:
            return jsonify({"code": OK})


@house_blue.route('/new_house/')
@login_required
def new_house():
    if request.method == 'GET':
        return render_template('newhouse.html')


@house_blue.route('/area_info/')
def area_info():
    if request.method == 'GET':
        area_info = Area.query.all()
        facility = Facility.query.all()
        facility_infos = []
        all_info = []
        for area in area_info:
            info = area.to_dict()
            all_info.append(info)
        for fac in facility:
            info = fac.to_dict()
            facility_infos.append(info)
        return jsonify(all_info, facility_infos)


@house_blue.route('/up_house/', methods=['POST'])
@login_required
def up_house():
    if request.method == 'POST':
        user = current_user
        user_id = user.id
        title = request.form.get('title')
        price = int(request.form.get('price'))
        area_id = int(request.form.get('area_id'))
        address = request.form.get('address')
        room_count = int(request.form.get('room_count'))
        acreage = int(request.form.get('acreage'))
        unit = request.form.get('unit')
        capacity = int(request.form.get('capacity'))
        beds = request.form.get('beds')
        deposit = int(request.form.get('deposit'))
        min_days = int(request.form.get('min_days'))
        max_days = int(request.form.get('max_days'))
        facilitys = request.form.getlist('facility')
        house = House()
        house.user_id = user_id
        house.area_id = area_id
        house.title = title
        house.price = price
        house.address = address
        house.room_count = room_count
        house.acreage = acreage
        house.unit = unit
        house.capacity = capacity
        house.beds = beds
        house.deposit = deposit
        house.min_days = min_days
        house.max_days = max_days
        for facility in facilitys:
            house_facility = Facility.query.filter_by(id=int(facility)).first()
            house.facilities.append(house_facility)
        house.add_update()
        house_id = house.id
        return jsonify({"code": OK, "house_id": house_id})


@house_blue.route('/up_house_image/', methods=['POST'])
@login_required
def up_house_image():
    if request.method == 'POST':
        image = request.files.get('house_image')
        house_id = int(request.form.get('house_id'))
        if is_graph(image.filename):
            image_path = os.path.join(UPLOAD_DIR, image.filename)
            image.save(image_path)
            house = House.query.get(house_id)
            house.index_image_url = os.path.join('upload', image.filename)
            house.add_update()
            house_image = HouseImage()
            house_image.house_id = house_id
            house_image.url = os.path.join('upload', image.filename)
            house_image.add_update()
            return jsonify({"code": OK})
        else:
            return jsonify({"code": IMAGE_FORMAT_ERROR})


@house_blue.route('/house_detail/<int:house_id>/')
@login_required
def house_detail(house_id):
    if request.method == 'GET':
        session["house_id"] = house_id
        return render_template('detail.html')


@house_blue.route('/house_detail_info/')
@login_required
def house_detail_info():
    if request.method == 'GET':
        house_id = int(session.get("house_id"))
        house_obj = House.query.get(house_id)
        info = house_obj.to_full_dict()
        if house_obj.user_id == current_user.id:
            info["booking"] = 0
        else:
            info["booking"] = 1
        return jsonify(info)





