import pymysql
from pymysql.cursors import DictCursor

class DBUtils:
    """数据库操作工具类"""
    
    def __init__(self, host='localhost', port=3306, user='root', 
                 password='123456', database='test_db'):
        self.connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            cursorclass=DictCursor  # 返回字典格式，方便取值
        )
    
    def execute_query(self, sql, params=None):
        """执行查询，返回所有结果"""
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    
    def execute_one(self, sql, params=None):
        """执行查询，返回单条结果"""
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()
    
    def execute_update(self, sql, params=None):
        """执行更新/插入/删除，返回影响的行数"""
        with self.connection.cursor() as cursor:
            rows = cursor.execute(sql, params)
            self.connection.commit()
            return rows
    
    def close(self):
        """关闭数据库连接"""
        self.connection.close()
    
    def __enter__(self):
        """支持 with 语句"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出 with 语句时自动关闭连接"""
        self.close()


# 使用示例
if __name__ == '__main__':
    # 方式1：普通使用
    db = DBUtils()
    result = db.execute_one("SELECT 1 as num")
    print(result)  # {'num': 1}
    db.close()
    
    # 方式2：使用 with 语句（推荐，自动关闭连接）
    with DBUtils() as db:
        result = db.execute_one("SELECT 1 as num")
        print(result)