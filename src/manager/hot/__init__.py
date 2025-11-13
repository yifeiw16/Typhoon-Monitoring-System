from flask import render_template, flash, request, redirect, url_for, session, jsonify, Blueprint
from functools import wraps
from tools import MySQLTools

manager_hot = Blueprint('manager_hot', __name__)
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

@manager_hot.route('/main', methods = ['GET', 'POST'])
@login_required
def main():
    points = util.getPoints()
    if request.method == "POST":
        form = request.form
        typhoon_id = form.get('mytyphoon0')
        typhoon_location = form.get('mytyphoon1')
        typhoon_lon = form.get('mytyphoon2')
        typhoon_lat = form.get('mytyphoon3')
        if typhoon_id and typhoon_location and typhoon_lon and typhoon_lat:
            util.addtyphoon(typhoon_id, typhoon_location, typhoon_lon, typhoon_lat)
    return render_template("/manager/hot/hot.html", points = points)
