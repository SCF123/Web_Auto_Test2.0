"""
用例作者：scf
用例明细：
    test_open_custom_attribute(self):[人员管理]--[自定义属性]，验证自定义属性页面回显信息
    test_add_attribute(self):[人员管理]--[自定义属性]，新增一个属性
    test_update_attribute(self):[人员管理]--[自定义属性]，修改一个属性的内容
    test_del_attribute(self):[人员管理]--[自定义属性]，删除一个属性
    test_up_attribute(self):[人员管理]--[自定义属性]，上移一个属性
    test_down_attribute(self):[人员管理]--[自定义属性]，下移一个属性
"""

from selenium_lib import Pyse, TestCase, TestRunner
from testcase.common import platform_api


class Test_Custom_Attribute(TestCase):
    def add_attribute(self, attr_name):
        """添加一个属性"""
        self.click(".mr10:nth-child(1)")
        self.clear("xpath=>//input[@type='text']")
        self.type("xpath=>//input[@type='text']", attr_name)
        self.sleep(1)
        self.click(".menuMgt-model:nth-child(3) .ivu-btn-primary > span")
        self.sleep(1)

    def del_attribute(self, attr_name):
        """删除一个属性"""
        self.sleep(2)
        self.click(f"xpath=>//span[contains(.,'{attr_name}')]")
        self.click(".mr10:nth-child(4)")
        self.sleep(1)
        self.click(".tenant-model .ivu-btn-primary > span")
        if "删除成功！" != self.get_text(".ivu-message span"):
            self.F5()
            platform_api.open_page(self, 2, "自定义属性")
            self.click(f"xpath=>//span[contains(.,'{attr_name}')]")
            self.click(".mr10:nth-child(4)")
            self.click(".tenant-model .ivu-btn-primary > span")
        self.sleep(2)

    @classmethod
    def setUpClass(cls):
        cls.driver = Pyse("chrome")
        platform_api.login_platform(cls.driver)

    def test_open_custom_attribute(self):
        """[人员管理]--[自定义属性]，验证自定义属性页面回显信息"""
        platform_api.open_page(self, 2, "自定义属性")

        # 验证[添加]按钮是否存在
        self.assertTrue(self.element_is_exist(".mr10:nth-child(1)"))

        # 验证[上移]按钮是否存在
        self.assertTrue(self.element_is_exist(".mr10:nth-child(2)"))

        # 验证[下移]按钮是否存在
        self.assertTrue(self.element_is_exist(".mr10:nth-child(3)"))

        # 验证[删除]按钮是否存在
        self.assertTrue(self.element_is_exist(".mr10:nth-child(4)"))

        # 验证[修改]按钮是否存在
        self.assertTrue(self.element_is_exist(".ivu-btn:nth-child(5)"))

    def test_add_attribute(self):
        """[人员管理]--[自定义属性]，新增一个属性"""
        platform_api.open_page(self, 2, "自定义属性")

        # 添加一个属性
        self.click(".mr10:nth-child(1)")
        self.clear("xpath=>//input[@type='text']")
        self.type("xpath=>//input[@type='text']", "属性1")
        # 是否必须：false
        # self.sleep(1)
        self.click("xpath=>//i[2]")
        self.click(".ivu-select-visible .ivu-select-item:nth-child(2)")
        # 属性类型：单选
        self.sleep(1)
        self.click("xpath=>//div[3]/div/div/div/i[2]")
        self.click(".ivu-select-visible .ivu-select-item:nth-child(2)")
        # 添加选项
        self.sleep(1)
        self.click(".ivu-btn-small:nth-child(2) > span")
        self.clear(".ivu-form-item-content > .ivu-form-item .ivu-input")
        self.type(".ivu-form-item-content > .ivu-form-item .ivu-input", "男")
        self.click(".ivu-btn-small:nth-child(3) > span")
        self.clear(".ivu-input-wrapper:nth-child(2) > .ivu-input")
        self.type(".ivu-input-wrapper:nth-child(2) > .ivu-input", "女")
        self.click(".ivu-btn-small:nth-child(4) > span")
        self.clear(".ivu-form-item:nth-child(3) > .ivu-form-item-content:nth-child(1) .ivu-input")
        self.type(".ivu-form-item:nth-child(3) > .ivu-form-item-content:nth-child(1) .ivu-input", "其他")
        # 删除 其他
        self.click(".ivu-form-item:nth-child(3) a")
        # 确定
        self.click(".menuMgt-model:nth-child(3) .ivu-btn-primary > span")

        # 验证添加属性是否成功
        self.sleep(2)
        num = len(self.get_elements("xpath=>//tbody[@class='ivu-table-tbody']/tr"))
        attrs = []
        for i in range(1, num+1):
            attr = self.get_text(f"xpath=>//tr[{i}]/td/div/span[2]")
            attrs.append(attr)
        self.assertIn("属性1", attrs)

        # 验证属性是否出现在[账号管理]--[新增账号]弹窗页面
        platform_api.open_page(self, 2, "账号管理")
        self.click(".mt16 > span")
        self.sleep(1)
        name = self.get_text(".ivu-row:nth-child(2) .ivu-col:nth-child(2) .ivu-form-item-label")
        attr_name = name.split("：")[0]
        self.assertEqual("属性1", attr_name)

        # 清除测试数据
        self.sleep(1)
        platform_api.open_page(self, 2, "自定义属性")
        self.del_attribute("属性1")

    def test_update_attribute(self):
        """[人员管理]--[自定义属性]，修改一个属性的内容"""
        platform_api.open_page(self, 2, "自定义属性")

        # 先添加一个属性
        self.add_attribute("属性2")

        # 修改属性
        self.sleep(1)
        self.click("xpath=>//span[contains(.,'属性2')]")
        self.click(".ivu-btn:nth-child(5) > span")
        self.clear(".menuMgt-model:nth-child(4) .ivu-input:nth-child(2)")
        self.type(".menuMgt-model:nth-child(4) .ivu-input:nth-child(2)", "属性2改")
        self.click(".menuMgt-model:nth-child(4) .ivu-btn-primary > span")

        # 验证属性修改是否成功
        self.sleep(2)
        num = len(self.get_elements("xpath=>//tbody[@class='ivu-table-tbody']/tr"))
        attrs = []
        for i in range(1, num + 1):
            attr = self.get_text(f"xpath=>//tr[{i}]/td/div/span[2]")
            attrs.append(attr)
        self.assertIn("属性2改", attrs)

        # 清除测试数据
        self.del_attribute("属性2改")

    def test_del_attribute(self):
        """[人员管理]--[自定义属性]，删除一个属性"""
        platform_api.open_page(self, 2, "自定义属性")

        # 先添加一个属性
        self.add_attribute("属性3")

        # 删除属性
        self.sleep(1)
        self.del_attribute("属性3")

        # 验证属性删除是否成功
        attrs = []
        if self.element_is_exist("xpath=>//tbody[@class='ivu-table-tbody']/tr"):
            num = len(self.get_elements("xpath=>//tbody[@class='ivu-table-tbody']/tr"))
            for i in range(1, num + 1):
                attr = self.get_text(f"xpath=>//tr[{i}]/td/div/span[2]")
                attrs.append(attr)

        self.assertNotIn("属性3", attrs)

    def test_up_attribute(self):
        """[人员管理]--[自定义属性]，上移一个属性"""
        platform_api.open_page(self, 2, "自定义属性")

        # 先添加两个属性
        self.add_attribute("属性4")
        self.sleep(1)
        self.add_attribute("属性5")

        # 上移属性5
        self.sleep(3)
        self.click("xpath=>//span[contains(.,'属性5')]")
        self.click(".mr10:nth-child(2)")

        # 验证上移属性是否成功
        text = self.get_text(".ivu-message .ivu-message-success >span")
        self.assertEqual(text, "移动成功")

        # 清除测试数据
        self.del_attribute("属性4")
        self.del_attribute("属性5")

    def test_down_attribute(self):
        """[人员管理]--[自定义属性]， 下移一个属性"""
        platform_api.open_page(self, 2, "自定义属性")

        # 先添加两个属性
        self.add_attribute("属性6")
        self.sleep(1)
        self.add_attribute("属性7")

        # 下移属性5
        self.sleep(3)
        self.click("xpath=>//span[contains(.,'属性6')]")
        self.click(".mr10:nth-child(3)")

        # 验证下移属性是否成功
        text = self.get_text(".ivu-message .ivu-message-success >span")
        self.assertEqual(text, "移动成功")

        # 清除测试数据
        self.del_attribute("属性7")
        self.del_attribute("属性6")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    TestRunner().debug()
