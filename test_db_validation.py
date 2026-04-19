import pytest
import requests
from db_utils import DBUtils


class TestDBValidation:
    """数据库校验测试类"""
    
    @pytest.fixture
    def db(self):
        """数据库 fixture，自动管理连接"""
        with DBUtils() as db:
            yield db
    
    # ========== 1. API 创建数据后，验证数据库 ==========
    def test_create_user_and_verify_db(self, db):
        """测试创建用户，验证数据库写入正确"""
        
        # 1. 准备测试数据
        test_user = {
            'username': 'testuser_001',
            'email': 'test001@example.com',
            'phone': '13800138001'
        }
        
        # 2. 调用 API 创建用户（示例用 httpbin）
        response = requests.post(
            'https://httpbin.org/post',
            json=test_user
        )
        assert response.status_code == 200
        
        # 3. 查询数据库验证用户是否存在
        sql = "SELECT * FROM users WHERE username = %s"
        result = db.execute_one(sql, (test_user['username'],))
        
        # 4. 断言数据库中的值
        assert result is not None, "数据库中未找到该用户"
        assert result['email'] == test_user['email']
        assert result['phone'] == test_user['phone']
    
    # ========== 2. 对比 API 返回数据和数据库数据 ==========
    def test_compare_api_with_db(self, db):
        """验证 API 返回的数据与数据库一致"""
        
        # 调用 API 获取用户列表
        response = requests.get('https://api.example.com/users')
        api_users = response.json()
        
        # 查询数据库获取用户列表
        db_users = db.execute_query("SELECT id, name, email FROM users WHERE status = 1")
        
        # 验证数量一致
        assert len(api_users) == len(db_users)
        
        # 逐条对比数据
        for api_user, db_user in zip(api_users, db_users):
            assert api_user['id'] == db_user['id']
            assert api_user['name'] == db_user['name']
            assert api_user['email'] == db_user['email']
    
    # ========== 3. 测试前置：清理测试数据 ==========
    def test_cleanup_before_test(self, db):
        """测试前清理测试数据，保证环境干净"""
        
        # 删除测试数据
        db.execute_update("DELETE FROM users WHERE username LIKE 'test_%'")
        
        # 验证已删除
        result = db.execute_one("SELECT COUNT(*) as cnt FROM users WHERE username LIKE 'test_%'")
        assert result['cnt'] == 0
    
    # ========== 4. 验证数据完整性 ==========
    def test_data_integrity(self, db):
        """验证必填字段不为空"""
        
        sql = "SELECT * FROM users WHERE username IS NULL OR email IS NULL"
        result = db.execute_query(sql)
        
        assert len(result) == 0, f"发现 {len(result)} 条数据存在空字段"
    
    # ========== 5. 验证唯一性约束 ==========
    def test_unique_constraint(self, db):
        """验证用户名唯一性"""
        
        # 查询是否有重复的用户名
        sql = """
            SELECT username, COUNT(*) as cnt 
            FROM users 
            GROUP BY username 
            HAVING cnt > 1
        """
        duplicates = db.execute_query(sql)
        
        assert len(duplicates) == 0, f"发现重复用户名: {duplicates}"
    
    # ========== 6. 事务回滚示例（测试失败时不影响数据库）==========
    def test_with_transaction_rollback(self, db):
        """测试事务回滚，失败时数据不会真正写入"""
        
        try:
            # 开始事务
            db.connection.begin()
            
            # 插入测试数据
            db.execute_update(
                "INSERT INTO users (username, email) VALUES (%s, %s)",
                ('temp_user', 'temp@test.com')
            )
            
            # 故意制造一个错误（比如查询不存在的表）
            db.execute_query("SELECT * FROM non_exist_table")
            
            # 如果上面没报错，提交事务
            db.connection.commit()
            
        except Exception as e:
            # 发生错误，回滚事务
            db.connection.rollback()
            print(f"事务回滚: {e}")
            raise
        
        # 验证数据没有被插入
        result = db.execute_one("SELECT * FROM users WHERE username = 'temp_user'")
        assert result is None


# ========== 7. 独立的测试函数（不使用 fixture）==========
def test_direct_db_query():
    """直接查询数据库示例"""
    with DBUtils() as db:
        # 查询用户数量
        result = db.execute_one("SELECT COUNT(*) as total FROM users")
        print(f"当前用户总数: {result['total']}")
        
        # 查询所有用户
        users = db.execute_query("SELECT id, username FROM users LIMIT 10")
        for user in users:
            print(f"用户ID: {user['id']}, 用户名: {user['username']}")