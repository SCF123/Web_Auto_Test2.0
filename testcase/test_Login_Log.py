"""
用例作者：scf
用例明细：
    test_open_login_log(self):[登录日志]--验证登录日志页面回显信息
    test_query_by_username(self):[登录日志]--根据用户名查询登录日志
    test_query_by_ip(self):[登录日志]--根据IP查询登录日志
    test_query_by_login_type(self):[登录日志]--根据日志类型查询登录日志
    test_query_by_datetime(self):[登录日志]--根据时间段查询登录日志
    test_query_reset(self):[登录日志]--重置搜索条件
"""

from selenium_lib import Pyse, TestCase, TestRunner
from testcase.common import platform_api
import datetime


class Test_Login_Log(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = Pyse("chrome")
        cls.driver.maximize_window()
        platform_api.login_platform(cls.driver)

    def test_open_login_log(self):
        """[登录日志]--验证登录日志页面回显信息"""
        platform_api.open_page(self, 1, "日志管理", "登录日志")

        # 验证[用户名]输入框是否存在
        self.assertTrue(self.element_is_exist("xpath=>//input[@type='text']"))

        # 验证[IP]地址输入框是否存在
        self.assertTrue(self.element_is_exist("xpath=>(//input[@type='text'])[2]"))

        # 验证[日志类型]下拉选择框是否存在
        self.assertTrue(self.element_is_exist("xpath=>//i[2]"))

        # 验证[开始时间]输入框是否存在
        self.assertTrue(self.element_is_exist(".ivu-col:nth-child(1) .ivu-date-picker .ivu-input"))

        # 验证[结束时间]输入框是否存在
        self.assertTrue(self.element_is_exist(".ivu-col:nth-child(2) .ivu-date-picker .ivu-input"))

        # 验证[查询]按钮是否存在
        self.assertTrue(self.element_is_exist(".mg10"))

        # 验证[重置]按钮是否存在
        self.assertTrue(self.element_is_exist(".mg16"))

    def test_query_by_username(self):
        """[登录日志]--根据用户名查询登录日志"""
        platform_api.open_page(self, 1, "日志管理", "登录日志")

        # 根据用户名查询登录日志
        self.clear("xpath=>//input[@type='text']")
        self.type("xpath=>//input[@type='text']", platform_api.plat_account)
        self.click(".mg10")

        # 验证查询结果是否正确
        self.sleep(2)
        num = len(self.get_elements("#tr_Root_undefined"))
        for i in range(1, num + 1):
            user_name = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[1]/div/span)[{i}]")
            self.assertEqual(platform_api.plat_account, user_name)

    def test_query_by_ip(self):
        """[登录日志]--根据IP查询登录日志"""
        platform_api.open_page(self, 1, "日志管理", "登录日志")

        # 根据IP查询查询登录日志
        ip = platform_api.get_host_ip()
        self.clear("xpath=>(//input[@type='text'])[2]")
        self.type("xpath=>(//input[@type='text'])[2]", ip)
        self.click(".mg10")

        # 验证查询结果是否正确
        self.sleep(2)
        num = len(self.get_elements("#tr_Root_undefined"))
        for i in range(1, num + 1):
            ip_addr = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/span)[{i}]")
            self.assertEqual(ip, ip_addr)

    def test_query_by_login_type(self):
        """[登录日志]--根据日志类型查询登录日志"""
        platform_api.open_page(self, 1, "日志管理", "登录日志")

        # 根据日志类型查询登录日志
        self.click(".w200 .ivu-icon-ios-arrow-down")
        self.sleep(1)
        # 选择 登录日志 类型
        self.click(".ivu-select-dropdown-transfer .ivu-select-item:nth-child(2)")
        self.click(".mg10")

        # 验证查询结果是否正确
        self.sleep(2)
        num = len(self.get_elements("#tr_Root_undefined"))
        for i in range(1, num + 1):
            login_type = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[3]/div/span)[{i}]")
            self.assertEqual("登录", login_type[:2])

    def test_query_by_datetime(self):
        """[登录日志]--根据时间段查询登录日志"""
        platform_api.open_page(self, 1, "日志管理", "登录日志")

        # 根据时间段查询登录日志
        now_time = datetime.datetime.now()
        now_str = now_time.strftime('%Y-%m-%d %H:%M:%S')
        time_ago = now_time - datetime.timedelta(days=3)
        str_ago = time_ago.strftime('%Y-%m-%d %H:%M:%S')
        self.clear("xpath=>(//input[@type='text'])[3]")
        self.type("xpath=>(//input[@type='text'])[3]", str_ago)
        self.clear("xpath=>(//input[@type='text'])[4]")
        self.type("xpath=>(//input[@type='text'])[4]", now_str)
        self.click(".mg10")

        # 验证查询的结果是否正确
        self.sleep(2)
        num = len(self.get_elements("#tr_Root_undefined"))
        for i in range(1, num + 1):
            login_time = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[4]/div/span)[{i}]")
            self.assertTrue(platform_api.compare_time(login_time, time_ago, now_time))

    def test_query_reset(self):
        """[登录日志]--重置搜索条件"""
        platform_api.open_page(self, 1, "日志管理", "登录日志")

        # 输入用户名
        self.clear("xpath=>//input[@type='text']")
        self.type("xpath=>//input[@type='text']", platform_api.plat_account)
        # 输入IP
        ip = platform_api.get_host_ip()
        self.clear("xpath=>(//input[@type='text'])[2]")
        self.type("xpath=>(//input[@type='text'])[2]", ip)
        # 选择登录类型
        self.click(".w200 .ivu-icon-ios-arrow-down")
        self.sleep(1)
        self.click(".ivu-select-dropdown-transfer .ivu-select-item:nth-child(3)")
        # 输入开始时间
        now_time = datetime.datetime.now()
        now_str = now_time.strftime('%Y-%m-%d %H:%M:%S')
        time_ago = now_time - datetime.timedelta(days=3)
        str_ago = time_ago.strftime('%Y-%m-%d %H:%M:%S')
        self.clear("xpath=>(//input[@type='text'])[3]")
        self.type("xpath=>(//input[@type='text'])[3]", str_ago)
        # 输入结束时间
        self.clear("xpath=>(//input[@type='text'])[4]")
        self.type("xpath=>(//input[@type='text'])[4]", now_str)

        # 重置搜索条件
        self.sleep(1)
        self.click(".mg16")

        # 验证条件重置是否成功
        self.sleep(1)
        user_name = self.get_attribute("xpath=>//input[@type='text']", "value")
        self.assertEqual("", user_name)

        ip = self.get_attribute("xpath=>(//input[@type='text'])[2]", "value")
        self.assertEqual("", ip)

        login_type = self.get_text(".w200 .ivu-select-selection")
        self.assertEqual("请选择", login_type)

        start_time = self.get_attribute("xpath=>(//input[@type='text'])[3]", "value")
        self.assertEqual("", start_time)

        end_time = self.get_attribute("xpath=>(//input[@type='text'])[4]", "value")
        self.assertEqual("", end_time)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    TestRunner().debug()
