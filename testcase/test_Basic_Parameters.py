"""
用例作者：scf
用例明细:
    test_open_baseconfigure(self):[基础参数]--验证基础参数页面回显信息
    test_add_configure(self):[基础参数]--新增一个参数
    test_update_configure(self):[基础参数]--修改参数("测试参数")
    test_query_by_paracode(self):[基础参数]--根据参数编码查询参数
    test_query_by_paraname(self):[基础参数]--根据参数名称查询参数
    test_query_by_childstation(self):[基础参数]--根据所属子站查询参数
    test_query_by_status(self):[基础参数]--根据状态查询参数
    test_query_reset(self):[基础参数]--重置查询条件
"""

from selenium_lib import Pyse, TestCase, TestRunner
from testcase.common import platform_api
import unittest, random


class Test_Basic_Parameters(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = Pyse("chrome")
        platform_api.login_platform(cls.driver)

    def test_open_baseconfigure(self):
        """[基础参数]--验证基础参数页面回显信息"""
        platform_api.open_page(self, 1, "参数配置", "基础参数")

        # 验证[参数编码]输入框是否存在
        self.assertTrue(self.element_is_exist(".ivu-col:nth-child(1) .ivu-input"))

        # 验证[参数名称]输入框是否存在
        self.assertTrue(self.element_is_exist(".ivu-col:nth-child(2) .ivu-input"))

        # 验证[所属子站]标签是否存在
        self.assertTrue(self.element_is_exist(".ivu-col:nth-child(1) .ivu-select-placeholder"))

        # 验证[状态]标签是否存在
        self.assertTrue(self.element_is_exist(".ivu-col:nth-child(2) .ivu-select-selected-value"))

        # 验证[查询]按钮是否存在
        self.assertTrue(self.element_is_exist(".ivu-form-item-content > .mg10"))

        # 验证[重置]按钮是否存在
        self.assertTrue(self.element_is_exist(".mg16"))

        # 验证[新增]按钮是否存在
        self.assertTrue(self.element_is_exist(".look > .ivu-btn-primary"))

        # 验证[修改]按钮是否存在
        self.assertTrue(self.element_is_exist(".mg10:nth-child(2)"))

    @unittest.skip("新增参数用例已执行通过，因无法删除新增的参数，故此处跳过不再执行")
    def test_add_configure(self):
        """[基础参数]--新增一个参数"""
        platform_api.open_page(self, 1, "参数配置", "基础参数")

        # 新增一个参数
        self.click(".look > .ivu-btn-primary")
        self.clear("xpath=>(//input[@type='text'])[3]")
        self.type("xpath=>(//input[@type='text'])[3]", "测试参数")
        self.clear("xpath=>(//input[@type='text'])[4]")
        self.type("xpath=>(//input[@type='text'])[4]", "test_code")
        self.click("xpath=>//div[3]/div/div/div/i[2]")
        self.sleep(1)
        self.click("xpath=>//li[contains(.,'数字')]")
        self.clear("xpath=>(//input[@type='text'])[5]")
        self.type("xpath=>(//input[@type='text'])[5]", "110110")
        self.click("xpath=>//div[5]/div/div/div/i[2]")
        self.sleep(1)
        self.click("xpath=>//div[3]/ul[2]/li[2]")  # 状态选择“不生效”
        self.sleep(1)
        self.click("xpath=>//div[6]/div/div/div/i[2]")
        self.sleep(2)
        self.click("xpath=>//div[4]/ul[2]/li[15]")  # 所属子站选择“质检系统”
        self.clear("xpath=>//textarea")
        self.type("xpath=>//textarea", "此参数用于测试 新增参数 功能")
        self.click("div:nth-child(4) .ivu-btn-primary > span")  # 点击 确定

        # 验证参数是否新增成功
        self.sleep(1)
        self.click(".ivu-col:nth-child(2) .icon:nth-child(4)")
        self.sleep(1)
        self.click(".ivu-select-visible .ivu-select-item:nth-child(2)")
        self.click(".ivu-form-item-content > .mg10")
        self.sleep(2)
        para_name = self.get_text("xpath=>//tr[@id='tr_Root_undefined']/td/div")
        self.assertEqual(para_name, "测试参数")

    def test_update_configure(self):
        """[基础参数]--修改参数--测试参数"""
        platform_api.open_page(self, 1, "参数配置", "基础参数")

        # 先查询出 “测试参数”
        self.click(".ivu-col:nth-child(2) .icon:nth-child(4)")
        self.sleep(1)
        self.click(".ivu-select-visible .ivu-select-item:nth-child(2)")
        self.click(".ivu-form-item-content > .mg10")

        # 修改“测试参数”
        para_name = "测试参数" + random.choice("ABCDEFGHIJKLMN")
        para_value = "110" + str(random.randint(100, 999))
        self.click("xpath=>//tr[@id='tr_Root_undefined']/td/div")
        self.click(".mg10:nth-child(2)")
        self.clear("xpath=>(//input[@type='text'])[6]")
        self.type("xpath=>(//input[@type='text'])[6]", para_name)
        self.clear("xpath=>(//input[@type='text'])[8]")
        self.type("xpath=>(//input[@type='text'])[8]", para_value)
        self.click("div:nth-child(5) .ivu-btn-primary > span")

        # 验证参数是否修改成功
        self.sleep(2)
        para = self.get_text("xpath=>//tr[@id='tr_Root_undefined']/td/div")
        self.assertEqual(para, para_name)

    def test_query_by_paracode(self):
        """[基础参数]--根据参数编码查询参数"""
        platform_api.open_page(self, 1, "参数配置", "基础参数")

        # 根据参数编码查询"版权"
        self.clear(".ivu-col:nth-child(1) .ivu-input")
        self.type(".ivu-col:nth-child(1) .ivu-input", "copyRightName")
        self.click(".ivu-form-item-content > .mg10")

        # 验证查询是否成功
        self.sleep(2)
        para_name = self.get_text("xpath=>//tr[@id='tr_Root_undefined']/td/div")
        self.assertEqual(para_name, "版权")

    def test_query_by_paraname(self):
        """[基础参数]--根据参数名称查询参数"""
        platform_api.open_page(self, 1, "参数配置", "基础参数")

        # 根据参数名称查询"版权"
        self.clear(".ivu-col:nth-child(2) .ivu-input")
        self.type(".ivu-col:nth-child(2) .ivu-input", "版权")
        self.click(".ivu-form-item-content > .mg10")

        # 验证查询是否成功
        self.sleep(2)
        para_name = self.get_text("xpath=>//tr[@id='tr_Root_undefined']/td/div")
        self.assertEqual(para_name, "版权")

    def test_query_by_childstation(self):
        """[基础参数]--根据所属子站查询参数"""
        platform_api.open_page(self, 1, "参数配置", "基础参数")

        # 根据子站查询参数
        self.click("xpath=>//i[2]")
        self.sleep(2)
        self.click(".ivu-select-visible .ivu-select-item:nth-child(2)")
        self.click(".ivu-form-item-content > .mg10")

        # 验证查询是否成功
        self.sleep(2)
        num = len(self.get_elements("#tr_Root_undefined"))
        for i in range(1, num + 1):
            para_childsta = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[4]/div/span)[{i}]")
            self.assertEqual(para_childsta, "平台")

    def test_query_by_status(self):
        """[基础参数]--根据状态查询参数"""
        platform_api.open_page(self, 1, "参数配置", "基础参数")

        # 根据状态查询参数
        self.click(".ivu-col:nth-child(2) .icon:nth-child(4)")
        self.sleep(1)
        self.click(".ivu-select-visible .ivu-select-item:nth-child(2)")
        self.click(".ivu-form-item-content > .mg10")

        # 验证查询是否成功
        self.sleep(2)
        num = len(self.get_elements("#tr_Root_undefined"))
        for i in range(1, num + 1):
            para_status = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[5]/div/div)[{i}]")
            self.assertEqual(para_status, "不生效")

    def test_query_reset(self):
        """[基础参数]--重置查询条件"""
        platform_api.open_page(self, 1, "参数配置", "基础参数")

        # 输入参数编码
        self.clear(".ivu-col:nth-child(1) .ivu-input")
        self.type(".ivu-col:nth-child(1) .ivu-input", "copyRightName")
        # 输入参数名称
        self.clear(".ivu-col:nth-child(2) .ivu-input")
        self.type(".ivu-col:nth-child(2) .ivu-input", "版权")
        # 选择子站
        self.click("xpath=>//i[2]")
        self.sleep(2)
        self.click("xpath=>//li[contains(.,'质检系统')]")
        # 选择状态
        self.click(".ivu-col:nth-child(2) .icon:nth-child(4)")
        self.sleep(1)
        self.click(".ivu-select-visible .ivu-select-item:nth-child(2)")

        # 点击[重置]按钮
        self.click(".mg16")

        # 验证是否重置成功
        self.sleep(1)
        self.assertEqual(self.get_attribute(".ivu-col:nth-child(2) .ivu-input", "value"), "")
        self.assertEqual(self.get_attribute(".ivu-col:nth-child(1) .ivu-input", "value"), "")
        self.assertEqual(self.get_text(".ivu-col:nth-child(1) .ivu-select-selection"), "请选择")
        self.assertEqual(self.get_text(".ivu-col:nth-child(2) .ivu-select-selection"), "生效")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    TestRunner().debug()
