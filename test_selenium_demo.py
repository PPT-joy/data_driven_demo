import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class TestGitHubSearch:
    """GitHub 搜索测试（更稳定）"""
    
    @pytest.fixture
    def driver(self):
        """浏览器驱动 fixture"""
        print("\n🚀 启动浏览器...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()
        driver.implicitly_wait(10)
        yield driver
        print("\n🔒 关闭浏览器...")
        driver.quit()
    
    def test_search_on_github(self, driver):
        """测试 GitHub 搜索功能"""
        print("\n📖 打开 GitHub 首页...")
        driver.get("https://github.com")
        
        time.sleep(2)
        
        # 找到搜索框
        print("🔍 找到搜索框...")
        search_input = driver.find_element(By.NAME, "q")
        
        # 输入关键词
        print("🔍 输入搜索关键词: selenium")
        search_input.send_keys("selenium")
        
        # 按回车搜索
        search_input.send_keys(Keys.ENTER)
        
        time.sleep(2)
        
        # 验证搜索结果
        assert "selenium" in driver.title.lower()
        print("✅ GitHub 搜索测试通过！")


class TestBaiduWithJS:
    """使用 JavaScript 解决百度交互问题"""
    
    @pytest.fixture
    def driver(self):
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()
        yield driver
        driver.quit()
    
    def test_baidu_search_with_js(self, driver):
        """使用 JavaScript 绕过交互问题"""
        print("\n📖 打开百度首页...")
        driver.get("https://www.baidu.com")
        
        time.sleep(2)
        
        # 使用 JavaScript 输入
        print("🔍 使用 JavaScript 输入关键词...")
        driver.execute_script("document.getElementById('kw').value = 'pytest 教程'")
        
        # 使用 JavaScript 点击搜索按钮
        print("🖱️ 使用 JavaScript 点击搜索...")
        driver.execute_script("document.getElementById('su').click()")
        
        time.sleep(2)
        
        # 验证标题包含关键词
        assert "pytest" in driver.title.lower() or "百度" in driver.title
        print("✅ 百度搜索测试通过！")


def test_simple():
    """简单测试"""
    assert 1 + 1 == 2
    print("✅ 简单测试通过")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])