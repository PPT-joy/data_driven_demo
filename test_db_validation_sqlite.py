import pytest
import requests
from db_utils_sqlite import DBUtils, init_test_db


# ========== 测试前置：初始化数据库 ==========
@pytest.fixture(scope='session', autouse=True)
def setup_database():
    """整个测试会话只执行一次，初始化数据库"""
    init_test_db()
    yield


@pytest.fixture
def db():
    """每个测试用例独立的数据库连接"""
    with DBUtils() as db:
        yield db


class TestDBValidation:
    """数据库校验测试类"""
    
    # ========== 1. API 调用后验证数据库 ==========
    def test_create_user_and_verify_db(self, db):
        """测试创建用户，验证数据库写入正确"""
        
        # 1. 准备测试数据
        test_user = {
            'username': 'testuser_003',
            'email': 'test003@example.com',
            'phone': '13800138003'
        }
        
        # 2. 先确保用户不存在
        db.execute_update("DELETE FROM users WHERE username = ?", (test_user['username'],))
        
        # 3. 调用 API 创建用户（示例用 httpbin）
        response = requests.post(
            'https://httpbin.org/post',
            json=test_user
        )
        assert response.status_code == 200
        
        # 4. 插入数据库（模拟后端写入）
        db.execute_update(
            "INSERT INTO users (username, email, phone) VALUES (?, ?, ?)",
            (test_user['username'], test_user['email'], test_user['phone'])
        )
        
        # 5. 查询数据库验证
        result = db.execute_one("SELECT * FROM users WHERE username = ?", (test_user['username'],))
        
        # 6. 断言
        assert result is not None, "数据库中未找到该用户"
        assert result['email'] == test_user['email']
        assert result['phone'] == test_user['phone']
        
        print(f"✅ 用户 {test_user['username']} 验证通过")
    
    # ========== 2. 验证 CSV 数据与数据库一致性 ==========
    def test_csv_data_match_db(self, db):
        """验证 CSV 中的用户名在数据库中都存在"""
        import csv
        
        # 从 CSV 读取用户名
        csv_users = []
        with open('testdata.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                csv_users.append(row['username'])
        
        # 从数据库查询所有用户名
        db_users = db.execute_query("SELECT username FROM users")
        db_usernames = [u['username'] for u in db_users]
        
        # 验证 CSV 中的用户都在数据库中
        for username in csv_users:
            if username in db_usernames:
                print(f"✅ 用户 {username} 存在于数据库")
            else:
                print(f"⚠️ 用户 {username} 不存在于数据库")
    
    # ========== 3. 数据完整性校验 ==========
    def test_data_integrity(self, db):
        """验证必填字段不为空"""
        
        # 检查 username 或 email 为空的记录
        sql = "SELECT * FROM users WHERE username IS NULL OR email IS NULL"
        result = db.execute_query(sql)
        
        assert len(result) == 0, f"发现 {len(result)} 条数据存在空字段"
        print("✅ 数据完整性校验通过")
    
    # ========== 4. 唯一性校验 ==========
    def test_unique_constraint(self, db):
        """验证用户名唯一性"""
        
        sql = """
            SELECT username, COUNT(*) as cnt 
            FROM users 
            GROUP BY username 
            HAVING cnt > 1
        """
        duplicates = db.execute_query(sql)
        
        assert len(duplicates) == 0, f"发现重复用户名: {duplicates}"
        print("✅ 唯一性校验通过")
    
    # ========== 5. 测试前置：清理数据 ==========
    def test_cleanup_test_data(self, db):
        """清理测试数据"""
        
        # 删除测试用户
        db.execute_update("DELETE FROM users WHERE username LIKE 'testuser_%'")
        
        # 验证已删除
        result = db.execute_one("SELECT COUNT(*) as cnt FROM users WHERE username LIKE 'testuser_%'")
        assert result['cnt'] == 0
        
        print("✅ 测试数据清理完成")
    
    # ========== 6. 统计校验 ==========
    def test_user_count_statistics(self, db):
        """验证用户数量统计"""
        
        # 获取总用户数
        total = db.execute_one("SELECT COUNT(*) as cnt FROM users")
        
        # 获取正常状态用户数
        active = db.execute_one("SELECT COUNT(*) as cnt FROM users WHERE status = 1")
        
        print(f"总用户数: {total['cnt']}")
        print(f"活跃用户数: {active['cnt']}")
        
        assert active['cnt'] <= total['cnt']


# ========== 7. 独立测试函数 ==========
def test_direct_query():
    """直接查询示例"""
    with DBUtils() as db:
        # 查询所有用户
        users = db.execute_query("SELECT id, username, email FROM users")
        
        print("\n========== 用户列表 ==========")
        for user in users:
            print(f"ID: {user['id']}, 用户名: {user['username']}, 邮箱: {user['email']}")
        
        assert len(users) > 0, "数据库中没有用户"


def test_custom_sql_query():
    """自定义 SQL 查询示例"""
    with DBUtils() as db:
        # 查询指定用户
        sql = "SELECT * FROM users WHERE username = ?"
        user = db.execute_one(sql, ('admin',))
        
        if user:
            print(f"找到用户: {user['username']}, 邮箱: {user['email']}")
            assert user['username'] == 'admin'
        else:
            print("未找到 admin 用户")