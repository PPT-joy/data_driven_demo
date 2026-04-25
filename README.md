# 接口自动化测试框架

基于 Python + Pytest + Requests 的接口自动化测试框架，支持数据驱动、数据库校验、Allure 报告生成。

## 技术栈

| 类别 | 技术 |
|------|------|
| 编程语言 | Python 3.8+ |
| 测试框架 | Pytest |
| 请求库 | Requests |
| 数据驱动 | CSV / Excel (Pandas) |
| 数据库 | SQLite / MySQL (PyMySQL) |
| 测试报告 | Allure |
| 版本控制 | Git |
| 性能测试 | JMeter |

## 项目结构
 data_driven_demo/
 conftest.py # pytest 共享 fixture
 test_data_driven.py # 数据驱动测试用例（CSV/Excel）
 test_db_validation.py # 数据库校验测试（MySQL）
test_db_validation_sqlite.py # 数据库校验测试（SQLite）
 test_with_db.py # 集成数据库的测试示例
 test_seleium_demo.py # Selenium UI 自动化示例
 db_utils.py # MySQL 数据库工具类
 db_utils_sqlite.py # SQLite 数据库工具类
 db_config.py # 数据库配置文件
 api_performance_test.jmx # JMeter 性能测试脚本
 testdata.csv # CSV 测试数据
 testdata.xlsx # Excel 测试数据
 requirements.txt # Python 依赖
 .gitignore # Git 忽略文件

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
# 运行所有测试
pytest -v

# 运行指定文件
pytest test_data_driven.py -v

# 显示 print 输出
pytest -v -s
# 生成测试数据
pytest --alluredir=./allure-results

# 生成并打开报告
allure serve ./allure-results
# 命令行运行 JMeter 脚本
jmeter -n -t api_performance_test.jmx -l result.jtl -e -o ./report
```

## 核心功能
### 1. 接口自动化测试
基于 Pytest + Requests，支持 GET/POST/PUT/DELETE 方法：
def test_get_request(base_url, session):
    response = session.get(f"{base_url}/get")
    assert response.status_code == 200
### 2. 数据驱动测试
支持 CSV 和 Excel 作为数据源：
@pytest.mark.parametrize("username,password,expected_code", load_csv_data())
def test_login(username, password, expected_code):
    response = requests.post(url, json={"username": username, "password": password})
    assert response.status_code == expected_code
### 3. 数据库校验
API 调用后自动校验数据库数据一致性：
def test_create_user_and_verify_db(self, db):
    # 调用 API 创建用户
    response = requests.post(url, json=test_user)
    # 查询数据库验证
    result = db.execute_one("SELECT * FROM users WHERE username = ?", (test_user['username'],))
    assert result['email'] == test_user['email']
### 4. 性能测试
JMeter 脚本配置：
50 并发用户;
10 秒 Ramp-Up;
聚合报告分析吞吐量和响应时间;

## 测试数据示例
CSV 文件格式：
username,password	,expected_code	expected_msg
admin,123456,200,success
guest,wrong,200,unauthorized
test,pass,200,success

## 环境要求
Python 3.8+
Chrome 浏览器（Selenium 测试需要）
JMeter 5.6.3（性能测试需要）

## 更新日志
2025.04：添加数据库校验测试模块
2025.04：添加 Selenium UI 自动化示例
2025.04：添加 JMeter 性能测试脚本
2025.03：完成接口自动化测试框架搭建