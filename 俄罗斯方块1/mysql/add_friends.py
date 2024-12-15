from gongju.tupian import globals
import pymysql
from pymysql import Connection
from pymysql.cursors import DictCursor

class MySQL:
    def look_user(self, username):
        self.conn = Connection(
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            database='user_pygame'  # 直接在连接时指定数据库
        )
        self.cursor = self.conn.cursor(DictCursor)
        try:
            # 查询指定用户名
            self.cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            for user in self.cursor.fetchall():
                # 匹配用户名
                if user['username'] == username:
                    globals.logged_in_user = username
                    return True
                else:
                    print("密码错误")
                    return False
            print("用户名不存在")
            return False
        except Exception as e:
            print(f"查询用户时出错: {e}")
            return False
        finally:
            # 关闭连接
            self.cursor.close()
            self.conn.close()

if __name__ == '__main__':
    mysql = MySQL()
    username = 'omega'
    print(mysql.look_user(username))
