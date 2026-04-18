import pytest
import csv
import pandas as pd
import requests

# ========== 方法一：使用 csv 模块（无需安装 pandas）==========
def test_login_from_csv():
    """从 CSV 文件读取测试数据"""
    with open('testdata.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            username = row['username']
            password = row['password']
            expected_code = int(row['expected_code'])
            
            # 发送请求（示例用 httpbin）
            response = requests.post(
                'https://httpbin.org/post',
                json={'username': username, 'password': password}
            )
            
            assert response.status_code == expected_code
            print(f"✅ {username} 测试通过")


# ========== 方法二：使用 pandas（功能更强）==========
def test_login_from_excel():
    """从 Excel 文件读取测试数据"""
    df = pd.read_excel('testdata.xlsx', engine='openpyxl')
    
    for index, row in df.iterrows():
        username = row['username']
        password = row['password']
        expected_code = row['expected_code']
        
        response = requests.post(
            'https://httpbin.org/post',
            json={'username': username, 'password': password}
        )
        
        assert response.status_code == expected_code
        print(f"✅ {username} 测试通过")


# ========== 方法三：使用 pytest 参数化 + CSV（推荐）==========
def load_csv_data(file_path):
    """加载 CSV 并返回列表格式，供 pytest 参数化使用"""
    data = []
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append((
                row['username'],
                row['password'],
                int(row['expected_code'])
            ))
    return data

@pytest.mark.parametrize("username,password,expected_code", load_csv_data('testdata.csv'))
def test_parametrized_from_csv(username, password, expected_code):
    """使用 pytest 参数化，每个用例独立显示"""
    response = requests.post(
        'https://httpbin.org/post',
        json={'username': username, 'password': password}
    )
    assert response.status_code == expected_code


# ========== 方法四：使用 pytest 参数化 + Excel ==========
def load_excel_data(file_path):
    """加载 Excel 并返回列表格式"""
    df = pd.read_excel(file_path, engine='openpyxl')
    return [(row['username'], row['password'], row['expected_code']) 
            for _, row in df.iterrows()]

@pytest.mark.parametrize("username,password,expected_code", load_excel_data('testdata.xlsx'))
def test_parametrized_from_excel(username, password, expected_code):
    """从 Excel 参数化测试"""
    response = requests.post(
        'https://httpbin.org/post',
        json={'username': username, 'password': password}
    )
    assert response.status_code == expected_code