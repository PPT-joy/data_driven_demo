import sqlite3
import os

class DBUtils:
    """SQLite 数据库操作工具类"""
    
    def __init__(self, db_path='test.db'):
        """
        初始化数据库连接
        :param db_path: 数据库文件路径，默认 test.db
        """
        self.db_path = db_path
        self.connection = None
        self._connect()
    
    def _connect(self):
        """建立数据库连接"""
        self.connection = sqlite3.connect(self.db_path)
        # 返回字典格式的行（类似 pymysql 的 DictCursor）
        self.connection.row_factory = sqlite3.Row
    
    def execute_query(self, sql, params=None):
        """执行查询，返回所有结果（列表，每个元素是字典）"""
        cursor = self.connection.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        # 将 Row 对象转换为字典
        return [dict(row) for row in rows]
    
    def execute_one(self, sql, params=None):
        """执行查询，返回单条结果（字典）"""
        cursor = self.connection.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        row = cursor.fetchone()
        cursor.close()
        return dict(row) if row else None
    
    def execute_update(self, sql, params=None):
        """执行更新/插入/删除，返回影响的行数"""
        cursor = self.connection.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        self.connection.commit()
        rows = cursor.rowcount
        cursor.close()
        return rows
    
    def execute_many(self, sql, params_list):
        """批量执行（如批量插入）"""
        cursor = self.connection.cursor()
        cursor.executemany(sql, params_list)
        self.connection.commit()
        rows = cursor.rowcount
        cursor.close()
        return rows
    
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# ========== 初始化数据库和表 ==========
def init_test_db(db_path='test.db'):
    """初始化测试数据库，创建表并插入测试数据"""
    
    with DBUtils(db_path) as db:
        # 创建 users 表
        db.execute_update('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL,
                phone TEXT,
                status INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 清空现有数据（避免重复）
        db.execute_update("DELETE FROM users")
        
        # 插入测试数据
        test_users = [
            ('admin', 'admin@test.com', '13800000000'),
            ('testuser1', 'test1@test.com', '13800000001'),
            ('testuser2', 'test2@test.com', '13800000002'),
        ]
        
        for username, email, phone in test_users:
            try:
                db.execute_update(
                    "INSERT INTO users (username, email, phone) VALUES (?, ?, ?)",
                    (username, email, phone)
                )
            except sqlite3.IntegrityError:
                pass  # 如果已存在则跳过
        
        print("✅ 数据库初始化完成")
        
        # 验证一下
        count = db.execute_one("SELECT COUNT(*) as cnt FROM users")
        print(f"当前用户数量: {count['cnt']}")


# 使用示例
if __name__ == '__main__':
    # 初始化数据库
    init_test_db()
    
    # 测试查询
    with DBUtils() as db:
        # 查询所有用户
        users = db.execute_query("SELECT id, username, email FROM users")
        for user in users:
            print(f"用户: {user['username']}, 邮箱: {user['email']}")
        
        # 查询单条
        admin = db.execute_one("SELECT * FROM users WHERE username = ?", ('admin',))
        print(f"Admin 信息: {admin}")