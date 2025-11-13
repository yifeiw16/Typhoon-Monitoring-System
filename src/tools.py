import pymysql

# 将pymysql的查询结果转化为json格式
def sql_fetch_json(cursor: pymysql.cursors.Cursor):
    keys = []
    for column in cursor.description:
        keys.append(column[0])
    key_number = len(keys)

    json_data = []
    for row in cursor.fetchall():
        item = dict()
        for q in range(key_number):
            item[keys[q]] = row[q]
        json_data.append(item)
    return json_data

class MySQLTools():
    # 初始化
    def __init__(self, host, user, password, db, charset):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        self.conn = pymysql.connect(host = 'localhost', user = 'root', password = '123456', db = 'sharetyphoon', charset = 'utf8')
        self.cur = self.conn.cursor()

    # 创建数据库、表单，插入初始数据
    def create_all(self):
        with open('typhoon.sql', 'r', encoding = 'utf-8') as init_file:
            text = init_file.read()
            lines = text.split('----')
            for line in lines:
                self.cur.execute(line)
                if 'insert' in line or 'update' in line or 'delete' in line:
                    self.conn.commit()

    # 检查用户合法性
    def checkUserPassword(self, user_id, user_pass):
        sqlstr = f"select * from users where user_id = '{user_id}' and user_pass = '{user_pass}' limit 1;"
        self.cur.execute(sqlstr)
        result = self.cur.fetchone()
        return result != None

    # 检查管理员合法性
    def checkManagerPassword(self, manager_id, manager_pass):
        sqlstr = f"select * from manager where work_id = '{manager_id}' and manager_pass = '{manager_pass}' limit 1;"
        self.cur.execute(sqlstr)
        result = self.cur.fetchone()
        return result != None

    # 注册用户
    def registerUserAdmin(self, userid, username, useremail, userpass):
        sqlstr = "select user_pass from users where user_name = '" + username + "';"
        self.cur.execute(sqlstr)
        result = self.cur.fetchall()
        if result:
            return "existed"
        sqlstr = "insert into users(user_id, user_name, user_email, user_pass) values('" + userid + "','" + username + "','" \
                                    + useremail + "','" + userpass + "');"
        self.cur.execute(sqlstr)
        # 涉及写操作注意提交
        self.conn.commit()

    # 注册管理员
    def registerManagerAdmin(self, userid, username, useremail, userpass):
        sqlstr = "select manager_pass from manager where manager_name = '" + username + "';"
        self.cur.execute(sqlstr)
        result = self.cur.fetchall()
        if result:
            return "existed"
        sqlstr = "insert into manager(work_id, manager_name, manager_email, manager_pass) values('" + userid + "','" + username + "','" \
                                    + useremail + "','" + userpass + "');"
        self.cur.execute(sqlstr)
        # 涉及写操作注意提交
        self.conn.commit()

    # 数据统计
    def dataStatic(self):
        sqlstr = "select count(*) as cnt from users;"
        self.cur.execute(sqlstr)
        users = self.cur.fetchone()
        sqlstr = "select count(*) as cnt from typhoon;"
        self.cur.execute(sqlstr)
        typhoon = self.cur.fetchone()
        sqlstr = "select count(*) as cnt from rent;"
        self.cur.execute(sqlstr)
        rent = self.cur.fetchone()
        sqlstr = "select count(*) as cnt from news;"
        self.cur.execute(sqlstr)
        news = self.cur.fetchone()

        print( "23111111111111",users[0], typhoon[0], rent[0], news[0])
        return users[0], typhoon[0], rent[0], news[0]

    # 登陆地点占比统计
    def numStatic(self):
        sqlstr = "select count(*) as cnt from typhoon where typhoon_location = 'motyphoon';"
        self.cur.execute(sqlstr)
        n1 = self.cur.fetchone()[0]
        sqlstr = "select count(*) as cnt from typhoon where typhoon_location = 'OfO';"
        self.cur.execute(sqlstr)
        n2 = self.cur.fetchone()[0]
        sqlstr = "select count(*) as cnt from typhoon where typhoon_location = '哈啰';"
        self.cur.execute(sqlstr)
        n3 = self.cur.fetchone()[0]
        sqlstr = "select count(*) as cnt from typhoon where typhoon_location = 'utyphoon';"
        self.cur.execute(sqlstr)
        n4 = self.cur.fetchone()[0]
        n = n1 + n2 + n3 + n4
        return 1,2,3,4
        return int(n1 / n * 100), int(n2 / n * 100), int(n3 / n * 100), int(n4 / n * 100)

    # 时间序列统计
    def timeDataStatic(self):
        user_list, typhoon_list, rent_list, news_list = [], [], [], []
        years = [23, 24, 24, 24, 24, 24, 24]
        months = [12, 1, 2, 3, 4, 5, 6, 7]
        for i in range(len(years)):
            sqlstr = f"select count(*) as cnt from users where user_time >= '20{years[i]}-{months[i]:02d}-01 00:00:00' and user_time < '20{years[i]}-{months[i + 1]:02d}-01 00:00:00'"
            self.cur.execute(sqlstr)
            user_list.append(self.cur.fetchone()[0])
        for i in range(len(years)):
            sqlstr = f"select count(*) as cnt from typhoon where typhoon_time >= '20{years[i]}-{months[i]:02d}-01 00:00:00' and typhoon_time < '20{years[i]}-{months[i + 1]:02d}-01 00:00:00'"
            self.cur.execute(sqlstr)
            typhoon_list.append(self.cur.fetchone()[0])
        for i in range(len(years)):
            sqlstr = f"select count(*) as cnt from rent where rent_time >= '20{years[i]}-{months[i]:02d}-01 00:00:00' and rent_time < '20{years[i]}-{months[i + 1]:02d}-01 00:00:00'"
            self.cur.execute(sqlstr)
            rent_list.append(self.cur.fetchone()[0])
        for i in range(len(years)):
            sqlstr = f"select count(*) as cnt from news where news_created >= '20{years[i]}-{months[i]:02d}-01 00:00:00' and news_created < '20{years[i]}-{months[i + 1]:02d}-01 00:00:00'"
            self.cur.execute(sqlstr)
            news_list.append(self.cur.fetchone()[0])
        return user_list, typhoon_list, rent_list, news_list

    # 删除台风
    def deletetyphoon(self, typhoon_id):
        sqlstr = f"delete from typhoon where typhoon_id = '{typhoon_id}';"
        self.cur.execute(sqlstr)
        self.conn.commit()
        return

    # 删除用户
    def deleteUser(self, user_id):
        sqlstr = f"delete from users where user_id = '{user_id}';"
        self.cur.execute(sqlstr)
        self.conn.commit()
        return

    # 删除超级用户
    def deleteManager(self, work_id):
        sqlstr = f"delete from manager where work_id = '{work_id}';"
        self.cur.execute(sqlstr)
        self.conn.commit()
        return

    # 增添台风
    def addtyphoon(self, typhoon_id, typhoon_location, typhoon_time, typhoon_lon, typhoon_lat):
        sqlstr = f"insert ignore into typhoon(typhoon_id, typhoon_location, typhoon_time,typhoon_cnt, typhoon_lon, typhoon_lat, typhoon_status) values('{typhoon_id}','{typhoon_location}', '{typhoon_time}',0, {typhoon_lon}, {typhoon_lat}, 'false');"
        self.cur.execute(sqlstr)
        self.conn.commit()
        return

    # 添加用户
    def addUser(self, user_id, user_name, user_email, user_pass):
        sqlstr = f"insert ignore into users(user_id, user_name, user_email, user_pass) values('{user_id}','{user_name}', '{user_email}', '{user_pass}');"
        self.cur.execute(sqlstr)
        self.conn.commit()
        return

    # 添加超级用户
    def addManager(self, work_id, manager_name, manager_email, manager_pass):
        sqlstr = f"insert ignore into manager(work_id, manager_name, manager_email, manager_pass) values('{work_id}','{manager_name}', '{manager_email}', '{manager_pass}');"
        self.cur.execute(sqlstr)
        self.conn.commit()
        return

    # 所有台风信息
    def alltyphoonInfo(self):
        sqlstr = "select * from typhoon;"
        self.cur.execute(sqlstr)
        return sql_fetch_json(self.cur)

    # 所有租借信息
    def allRentInfo(self):
        sqlstr = "select * from rent;"
        self.cur.execute(sqlstr)
        return sql_fetch_json(self.cur)

    # 所有归还信息
    def allReturnInfo(self):
        sqlstr = "select * from retur;"
        self.cur.execute(sqlstr)
        return sql_fetch_json(self.cur)

    # # 个人租借信息
    # def personRentInfo(self, user_id):
    #     sqlstr = f"select * from rent where user_id = '{user_id}';"
    #     self.cur.execute(sqlstr)
    #     return sql_fetch_json(self.cur)

    def personRentInfo(self, user_id):
        sqlstr = f"""
        SELECT rent.*, retur.return_time, typhoon.*
        FROM rent
        LEFT OUTER JOIN retur ON rent._id_ = retur._id_ AND rent.user_id = retur.user_id AND rent.typhoon_id = retur.typhoon_id
        LEFT JOIN typhoon ON rent.typhoon_id = typhoon.typhoon_id
        WHERE rent.user_id = '{user_id}'
        ORDER BY rent.rent_time ASC;
        """
        self.cur.execute(sqlstr)
        return sql_fetch_json(self.cur)

    # 个人归还信息
    def personReturnInfo(self, user_id):
        sqlstr = f"select * from retur where user_id = '{user_id}';"
        self.cur.execute(sqlstr)
        return sql_fetch_json(self.cur)

    # 所有归还信息
    def allUserInfo(self):
        sqlstr = "select * from users;"
        print("?????????????????")
        self.cur.execute(sqlstr)
        return sql_fetch_json(self.cur)

    # 所有归还信息
    def allManagerInfo(self):
        sqlstr = "select * from manager;"
        self.cur.execute(sqlstr)
        return sql_fetch_json(self.cur)

    # 租借台风
    def renttyphoon(self, user_id, typhoon_id):
        sqlstr = f"SELECT COUNT(*) FROM rent WHERE user_id = '{user_id}' AND typhoon_id = '{typhoon_id}';"
        self.cur.execute(sqlstr)
        already_rented = self.cur.fetchone()[0] > 0

        if already_rented:
            # Update the rent time if the user has already rented the typhoon
            sqlstr = f"UPDATE rent SET rent_time = CURRENT_TIMESTAMP WHERE user_id = '{user_id}' AND typhoon_id = '{typhoon_id}';"
            self.cur.execute(sqlstr)
        else:
            # Insert into rent table if the user has not rented this typhoon before
            sqlstr = f"INSERT INTO rent(user_id, typhoon_id) VALUES('{user_id}','{typhoon_id}');"
            self.cur.execute(sqlstr)

            sqlstr = f"update typhoon set typhoon_cnt = typhoon_cnt + 1 where typhoon_id = '{typhoon_id}';"
            self.cur.execute(sqlstr)

            # Commit the transaction
            self.conn.commit()
        
        return

    # 取消关注
    def returntyphoon(self, user_id, typhoon_id):
        
        # sqlstr = f"select _id_ from rent where typhoon_id = '{typhoon_id}' order by _id_ desc;"
        # self.cur.execute(sqlstr)
        # id_list = self.cur.fetchall()
        # _id_ = id_list[0][0]
        # sqlstr = f"insert ignore into retur(_id_, user_id, typhoon_id) values('{_id_}', '{user_id}','{typhoon_id}');"
        # self.cur.execute(sqlstr)
        # self.conn.commit()

        # Delete the record from the rent table
        sqlstr = f"DELETE FROM rent WHERE user_id = '{user_id}' AND typhoon_id = '{typhoon_id}';"
        self.cur.execute(sqlstr)
        self.conn.commit()
        
        # 台风关注热度-1
        sqlstr = f"update typhoon set typhoon_cnt = typhoon_cnt - 1 where typhoon_id = '{typhoon_id}';"
        self.cur.execute(sqlstr)
        self.conn.commit()
        return

    # 台风查询
    def typhoon_userAll(self, typhoon_id):
        sqlstr = f"select rent.user_id, rent.typhoon_id, rent.rent_time, retur.return_time " \
                 f"from rent left outer join retur " \
                 f"on rent._id_ = retur._id_ and rent.user_id = retur.user_id and rent.typhoon_id = retur.typhoon_id " \
                 f"where rent.typhoon_id = '{typhoon_id}' " \
                 f"order by rent.rent_time asc;"
        self.cur.execute(sqlstr)
        return sql_fetch_json(self.cur)

    def update_typhoon_info(self, typhoon_id, typhoon_location, typhoon_time, typhoon_lon, typhoon_lat, typhoon_cnt):
        print("Updating typhoon info...")
        sqlstr = f"""
        UPDATE typhoon
        SET typhoon_location='{typhoon_location}', typhoon_time='{typhoon_time}', typhoon_lon='{typhoon_lon}', typhoon_lat='{typhoon_lat}', typhoon_cnt='{typhoon_cnt}'
        WHERE typhoon_id='{typhoon_id}';
        """
        print(sqlstr)
        self.cur.execute(sqlstr)
        self.conn.commit()
        return

    def getTyphoonInfoByLocation(self, location_query):
        sqlstr = "SELECT * FROM typhoon WHERE typhoon_location LIKE %s;"
        search_term = "%" + location_query + "%"  # 构建包含通配符的搜索词
        self.cur.execute(sqlstr, (search_term,))
        return sql_fetch_json(self.cur)



    # 用户查询
    def user_typhoonAll(self, user_id):
        sqlstr = f"select rent.user_id, rent.typhoon_id, rent.rent_time " \
                f"from rent " \
                f"where rent.user_id = '{user_id}' " \
                f"order by rent.rent_time asc;"

        
        self.cur.execute(sqlstr)
        return sql_fetch_json(self.cur)

    # 台风登陆地点分布热力图查询
    def getPoints(self):
        sqlstr = "select typhoon_lon, typhoon_lat from typhoon;"
        self.cur.execute(sqlstr)
        keys = ["lng", "lat"]
        json_data = []
        for row in self.cur.fetchall():
            item = dict()
            for q in range(2):
                item[keys[q]] = row[q]
            item["count"] = 100
            json_data.append(item)
        return json_data

    def news_All(self):
        sqlstr = f"select * from news;"
        self.cur.execute(sqlstr)
        return sql_fetch_json(self.cur)

    def news(self, news_id):
        sqlstr = f"select * from news where news_id = {news_id};"
        self.cur.execute(sqlstr)
        return sql_fetch_json(self.cur)

    def addNews(self, title, body, user):
        sqlstr = f"insert ignore into news (news_title, news_body, news_author, news_created, news_updated, total_views) values('{title}', '{body}', '{user}', current_timestamp, current_timestamp, 0);"
        self.cur.execute(sqlstr)
        self.conn.commit()
        return

    def deleteNews(self, news_id):
        sqlstr = f"delete from news where news_id = '{news_id}'"
        self.cur.execute(sqlstr)
        self.conn.commit()
        return

    def addNewsViews(self, news_id):
        sqlstr = f"update news set total_views = total_views + 1 where news_id = '{news_id}';"
        self.cur.execute(sqlstr)
        return

    def subNewsViews(self, news_id):
        sqlstr = f"update news set total_views = total_views - 1 where news_id = '{news_id}';"
        self.cur.execute(sqlstr)
        return

    def updateNews(self, news_id, title, body):
        sqlstr = f"update news set news_title = '{title}', news_body = '{body}', news_updated = current_timestamp where news_id = '{news_id}';"
        self.cur.execute(sqlstr)
        return
