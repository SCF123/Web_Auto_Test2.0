"""
用例作者：scf
用例明细：
    test_open_operation_log(self):[操作日志]--验证操作日志页面回显信息
    test_query_by_account(self):[操作日志]--根据账号查询操作日志
    test_query_by_operation_type(self):[操作日志]--根据操作分类查询操作日志
    test_query_by_datetime(self):[操作日志]--根据时间段查询操作日志
    test_query_reset(self):[操作日志]--重置搜索条件
"""

from selenium_lib import Pyse, TestCase, TestRunner
from testcase.common import platform_api
import datetime


class Test_Operation_Log(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = Pyse("chrome")
        cls.driver.maximize_window()
        platform_api.login_platform(cls.driver)

    def test_open_operation_log(self):
        """[操作日志]--验证操作日志页面回显信息"""
        platform_api.open_page(self, 1, "日志管理", "操作日志")

        # 验证[账号输入框]是否存在
        self.assertTrue(self.element_is_exist("xpath=>//input[@type='text']"))

        # 验证[操作分类下拉选择框]是否存在
        self.assertTrue(self.element_is_exist(".ivu-select-input"))

        # 验证[开始时间输入框是]否存在
        self.assertTrue(self.element_is_exist("xpath=>(//input[@type='text'])[3]"))

        # 验证[结束时间输入框]是否存在
        self.assertTrue(self.element_is_exist("xpath=>(//input[@type='text'])[4]"))

        # 验证[查询]按钮是否存在
        self.assertTrue(self.element_is_exist(".mg10"))

        # 验证[重置]按钮是否存在
        self.assertTrue(self.element_is_exist(".mg16"))

    def test_query_by_account(self):
        """[操作日志]--根据账号查询操作日志"""
        platform_api.open_page(self, 1, "日志管理", "操作日志")

        # 根据用户名查询登录日志
        self.clear("xpath=>//input[@type='text']")
        self.type("xpath=>//input[@type='text']", platform_api.plat_account)
        self.click(".mg10")

        # 验证查询结果是否正确
        self.sleep(2)
        num = len(self.get_elements("#tr_Root_undefined"))
        for i in range(1, num + 1):
            account = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[1]/div/span)[{i}]")
            self.assertEqual(platform_api.plat_account, account)

    def test_query_by_operation_type(self):
        """[操作日志]--根据操作分类查询操作日志"""
        # 先到[人员管理]-[组织管理]页面新建一个组织，以产生一条操作记录
        platform_api.open_page(self, 2, "组织管理")
        self.click(".mr10:nth-child(6) > span")
        self.sleep(1)
        self.clear("xpath=>(//input[@type='text'])[4]")
        self.type("xpath=>(//input[@type='text'])[4]", "操作测试")
        self.clear("xpath=>(//input[@type='text'])[5]")
        self.type("xpath=>(//input[@type='text'])[5]", "12321")
        self.click(".dpt-model:nth-child(3) .ivu-btn-primary > span")
        self.sleep(2)

        # 再进入操作日志页面
        platform_api.open_page(self, 1, "日志管理", "操作日志")

        # 选择 新增组织 操作分类
        self.click("xpath=>//i[2]")
        self.sleep(1)
        self.click("xpath=>//li[contains(.,'新增组织')]")
        self.click(".mg10")

        # 验证查询结果是否正确
        self.sleep(2)
        num = len(self.get_elements("#tr_Root_undefined"))
        for i in range(1, num + 1):
            op_type = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/span)[{i}]")
            self.assertEqual("新增组织", op_type)

        # 清除测试数据
        self.sleep(1)
        platform_api.open_page(self, 2, "组织管理")
        self.click("xpath=>//span[contains(.,'操作测试')]")
        self.click(".mr10:nth-child(3) > span")
        self.sleep(1)
        self.click(".tenant-model:nth-child(5) .ivu-btn-primary > span")
        self.sleep(1)

    def test_query_by_datetime(self):
        """[操作日志]--根据时间段查询操作日志"""
        platform_api.open_page(self, 1, "日志管理", "操作日志")

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
            op_time = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[3]/div/span)[{i}]")
            self.assertTrue(platform_api.compare_time(op_time, time_ago, now_time))

    def test_query_reset(self):
        """[操作日志]--重置搜索条件"""
        platform_api.open_page(self, 1, "日志管理", "操作日志")

        # 输入账号
        self.clear("xpath=>//input[@type='text']")
        self.type("xpath=>//input[@type='text']", platform_api.plat_account)
        # 选择删除组织 操作分类
        self.click("xpath=>//i[2]")
        self.sleep(1)
        self.click("xpath=>//li[contains(.,'删除组织')]")
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
        self.sleep(2)
        self.click(".mg16")

        # 验证条件重置是否成功
        self.sleep(1)
        account = self.get_attribute("xpath=>//input[@type='text']", "value")
        self.assertEqual("", account)

        op_type = self.get_attribute(".ivu-select-input", "value")
        self.assertEqual("", op_type)

        start_time = self.get_attribute("xpath=>(//input[@type='text'])[3]", "value")
        self.assertEqual("", start_time)

        end_time = self.get_attribute("xpath=>(//input[@type='text'])[4]", "value")
        self.assertEqual("", end_time)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    TestRunner().debug()
