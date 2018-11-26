from datetime import date, datetime
from operator import or_, and_

from flask import request, render_template, session, jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc

from utils.models import House, Order
from utils.status_code import *
from . import order_blue


@order_blue.route('/my_order/')
@login_required
def my_order():
    if request.method == 'GET':
        return render_template('orders.html')


@order_blue.route('/order_add/', methods=['POST'])
@login_required
def order_add():
    if request.method == 'POST':
        data = request.form
        order = Order(**data)
        order.user_id = current_user.id
        order.add_update()
        return jsonify({"code": OK})


@order_blue.route('/my_order_info/')
@login_required
def my_order_info():
    if request.method == 'GET':
        user_id = current_user.id
        orders = Order.query.filter(Order.user_id == user_id).all()
        info = [order.to_dict() for order in orders]
        return jsonify(info)


@order_blue.route('/comment_order/', methods=['POST'])
@login_required
def comment_order():
    if request.method == 'POST':
        order_id = int(request.form.get('order_id'))
        comment = request.form.get('comment')
        # 状态变更，从待评价到已完成
        order = Order.query.get(order_id)
        order.status = "COMPLETE"
        order.comment = comment
        # 更新房源出租次数
        house = House.query.filter(House.id == order.house_id).first()
        house.order_count = int(house.order_count) + 1
        house.add_update()
        order.add_update()
        return jsonify({'code': OK})


@order_blue.route('/cu_order/')
@login_required
def cu_order():
    if request.method == 'GET':
        return render_template('lorders.html')


@order_blue.route('/cu_order_info/')
@login_required
def cu_order_info():
    if request.method == 'GET':
        houses = House.query.filter_by(user_id=current_user.id).all()
        house_ids = [house.id for house in houses]
        orders = Order.query.filter(Order.house_id.in_(house_ids)).all()
        orders_info = [order.to_dict() for order in orders]
        return jsonify(orders=orders_info)


@order_blue.route('/accept_order/', methods=['POST'])
@login_required
def accept_order():
    if request.method == 'POST':
        order_id = int(request.form.get('order_id'))
        # 状态变更，从待接单到待评价
        order = Order.query.get(order_id)
        order.status = "WAIT_COMMENT"
        order.add_update()
        return jsonify({'code': OK})


@order_blue.route('/reject_order/', methods=['POST'])
@login_required
def reject_order():
    if request.method == 'POST':
        order_id = int(request.form.get('order_id'))
        comment = request.form.get('reject_reason')
        # 状态变更，从待接单到已拒单
        order = Order.query.get(order_id)
        order.status = "REJECTED"
        order.comment = comment
        order.add_update()
        return jsonify({'code': OK})


@order_blue.route('/booking/<int:house_id>/')
@login_required
def booking(house_id):
    if request.method == 'GET':
        session["house_id"] = house_id
        return render_template('booking.html')


@order_blue.route('/booking_info/')
@login_required
def booking_info():
    if request.method == 'GET':
        house_id = int(session.get("house_id"))
        house = House.query.get(house_id)
        info = house.to_dict()
        return jsonify(info)


@order_blue.route('/index/')
def index():
    if request.method == 'GET':
        return render_template('index.html')


@order_blue.route('/index_info/')
def index_info():
    if request.method == 'GET':
        orders = Order.query.all()
        booking_houses_id = [order.house_id for order in orders if order.status in ["WAIT_PAYMENT", "PAID", "WAIT_ACCEPT"]]
        houses = House.query.filter(~House.id.in_(booking_houses_id))
        final_houses = houses.order_by(desc('update_time'))
        info = [house.to_dict() for house in final_houses]
        return jsonify(info)


@order_blue.route('/check_user/')
@login_required
def check_user():
    if request.method == 'GET':
        user = current_user
        if user.is_authenticated:
            info = user.to_basic_dict()
            return jsonify({"code": OK, "info": info})
        else:
            return jsonify({"code": USER_HAS_NOT_LOGIN})


@order_blue.route('/search/')
def search():
    if request.method == 'GET':
        return render_template('search.html')


@order_blue.route('/search_info/', methods=['POST'])
def search_info():
    if request.method == 'POST':
        area_id = request.form.get('aid')
        start_time = request.form.get('sd')
        end_time = request.form.get('ed')
        if not start_time:
            start_time = date.today().strftime("%Y-%m-%d")
        sk = request.form.get('sk')
        # p = request.form.get('p')
        if end_time:
            start_date = datetime.strptime(start_time, '%Y-%m-%d')
            end_date = datetime.strptime(end_time, "%Y-%m-%d")
            differ_days = int((end_date-start_date).days)
            # 如果用户输入有开始和结束时间则显示数据库该分段的信息
            houses_first = House.query.filter(or_(and_(House.min_days <= differ_days, House.max_days >= differ_days),
                                                  and_(House.min_days <= differ_days, House.max_days == 0)))
        else:
            # 用户没有输入结束时间则显示所有信息
            houses_first = House.query.filter()
        if area_id:
            # 如果用户选择了区域信息
            houses_second = houses_first.filter(House.area_id == int(area_id))
        else:
            # 没有选择
            houses_second = houses_first
        # 过滤订单中的房源：待支付和已支付状态
        orders_filter = Order.query.filter(Order.status.in_(["WAIT_PAYMENT", "PAID", "WAIT_ACCEPT"])).all()
        # 去重房源id，因为过滤条件为待支付和已置夫，但还有完成后的订单记录，所以需要去重
        orders_filter_ids = set([order_filter.house_id for order_filter in orders_filter])
        houses_third = houses_second.filter(~House.id.in_(orders_filter_ids))
        # 排序
        # 新房源
        if sk == 'new':
            houses_final = houses_third.order_by(desc('update_time'))
        # 入住最多
        elif sk == 'booking':
            houses_final = houses_third.order_by(desc('order_count'))
        # 价格由高-低
        elif sk == 'price-inc':
            houses_final = houses_third.order_by('price')
        # 价格由低到高
        else:
            houses_final = houses_third.order_by(desc('price'))
        houses = houses_final.all()
        houses_info = [house.to_full_dict() for house in houses]
        return jsonify(houses_info)




