from flask import render_template, flash, request, redirect, url_for, session, jsonify, Blueprint
from functools import wraps
from tools import MySQLTools

manager_typhoon = Blueprint('manager_typhoon', __name__)
# 初始化数据库
util = MySQLTools('localhost', 'root', '123456', 'sharetyphoon', 'utf8')

# 判断用户是否登录成功
def login_required(func):
    @wraps(func)  # 继承原函数，调用时不改变函数原含义
    def wrapper(*args, **kwargs):
        if session.get('user', None):
            return func(*args, **kwargs)
        else:
            flash("请先登录", 'danger')
            return redirect(url_for('login'))
    return wrapper

@manager_typhoon.route('/add', methods = ['GET', 'POST'])
@login_required
def typhoon_add():
    if request.method == "POST":
        form = request.form
        typhoon_id = form.get('mytyphoon0')
        typhoon_location = form.get('mytyphoon1')
        typhoon_time = form.get('mytyphoon2')
        typhoon_lon = form.get('mytyphoon3')
        typhoon_lat = form.get('mytyphoon4')
        if typhoon_id and typhoon_location and typhoon_lon and typhoon_lat:
            util.addtyphoon(typhoon_id, typhoon_location,typhoon_time, typhoon_lon, typhoon_lat)
    return render_template("/manager/typhoon/typhoon_add.html")


@manager_typhoon.route('/look', methods = ['GET', 'POST'])
@login_required
def typhoon_look():
    return render_template("/manager/typhoon/typhoon_look.html")

@manager_typhoon.route('/delete', methods = ['GET', 'POST'])
@login_required
def typhoon_delete():
    if request.method == "POST":
        form = request.form
        typhoon_id = form.get('mytyphoon')
        if typhoon_id:
            util.deletetyphoon(typhoon_id)
    return render_template("/manager/typhoon/typhoon_delete.html")

@manager_typhoon.route('/rent', methods = ['GET', 'POST'])
@login_required
def typhoon_rent():
    if request.method == "POST":
        form = request.form
        typhoon_id = form.get('mytyphoon')
        if typhoon_id:
            util.renttyphoon(session['user'], typhoon_id)
    return render_template("/manager/typhoon/typhoon_rent.html")

@manager_typhoon.route('/return', methods = ['GET', 'POST'])
@login_required
def typhoon_return():
    if request.method == "POST":
        form = request.form
        typhoon_id = form.get('mytyphoon')
        if typhoon_id:
            util.returntyphoon(session['user'], typhoon_id)
    return render_template("/manager/typhoon/typhoon_return.html")

@manager_typhoon.route('/query', methods = ['GET', 'POST'])
@login_required
def typhoon_query():
    if request.method == "POST":
        form = request.form
        typhoonid = form.get('mytyphoon')
        if typhoonid:
            global typhoon_id
            typhoon_id = typhoonid
    return render_template("/manager/typhoon/typhoon_query.html")

@manager_typhoon.route('/typhoondata', methods=['POST', 'GET'])
def typhoon_data():
    data = util.alltyphoonInfo()
    if request.method == 'GET':
        info = request.values
        limit = info.get('limit', 10)
        offset = info.get('offset', 0)
    return jsonify({'total': len(data), 'rows': data[int(offset) : (int(offset) + int(limit))]})


@manager_typhoon.route('/update-typhoon-info', methods=['POST'])
def update_typhoon_info():
    # 获取前端发送的数据
    data = request.json
    typhoon_id = data['typhoon_id']
    typhoon_location = data['typhoon_location']
    typhoon_time = data['typhoon_time']
    typhoon_lon = data['typhoon_lon']
    typhoon_lat = data['typhoon_lat']
    typhoon_cnt = data['typhoon_cnt']

   
    util.update_typhoon_info(typhoon_id, typhoon_location, typhoon_time, typhoon_lon, typhoon_lat, typhoon_cnt)
    
    return jsonify({'status': 'success', 'message': '信息更新成功'})


@manager_typhoon.route('/rentdata', methods=['POST', 'GET'])
def rent_data():
    data = util.allRentInfo()
    if request.method == 'GET':
        info = request.values
        limit = info.get('limit', 10)
        offset = info.get('offset', 0)
    return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})

@manager_typhoon.route('/returndata', methods=['POST', 'GET'])
def return_data():
    data = util.allReturnInfo()
    if request.method == 'GET':
        info = request.values
        limit = info.get('limit', 10)
        offset = info.get('offset', 0)
    return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})

@manager_typhoon.route('/typhoonquerydata', methods=['POST', 'GET'])
def typhoon_query_data():
    global typhoon_id
    data = util.getTyphoonInfoByLocation(typhoon_id)
    if request.method == 'GET':
        info = request.values
        limit = info.get('limit', 10)
        offset = info.get('offset', 0)

    return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})

