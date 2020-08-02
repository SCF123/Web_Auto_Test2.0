"""
用例作者：scf
用例明细：
    test_open_menu_manage(self):[菜单管理]--验证菜单管理页面回显信息
    test_add_parent_menu(self):[菜单管理]新增一级菜单
    test_update_menu(self):[菜单管理]修改一级菜单
    test_add_second_menu(self):[菜单管理]新增一个二级菜单
    test_up_menu(self):[菜单管理]上移菜单
    test_down_menu(self):[菜单管理]下移菜单
    test_del_menu(self):[菜单管理]删除一个菜单
"""

from selenium_lib import Pyse, TestCase, TestRunner
from testcase.common import platform_api


class Test_Menu_Manage(TestCase):
    def add_menu(self, menu_name):
        """新增一个一级菜单"""
        self.click(".mr10:nth-child(2) > span")
        self.clear("xpath=>(//input[@type='text'])[2]")
        self.type("xpath=>(//input[@type='text'])[2]", menu_name)
        self.click(".icon-spread")
        self.click("#iconListR .icon-Person-manage")
        self.click("xpath=>//i[2]")
        self.click("xpath=>//li/span")
        self.click(".menuMgt-model:nth-child(3) .ivu-btn:nth-child(1) > span")

    def del_menu(self, menu_name):
        """删除一个菜单"""
        self.click(f"xpath=>//span[contains(.,'{menu_name}')]")
        self.click(".mr10:nth-child(5) > span")
        self.sleep(1)
        self.click(".tenant-model .ivu-btn-primary > span")
        self.sleep(1)

    @classmethod
    def setUpClass(cls):
        cls.driver = Pyse("chrome")
        platform_api.login_platform(cls.driver)

    def test_open_menu_manage(self):
        """[菜单管理]--验证菜单管理页面回显信息"""
        platform_api.open_page(self, 1, "菜单管理")

        # 验证[搜素输入框]是否存在
        self.assertTrue(self.element_is_exist(".search .ivu-input"))

        # 验证[搜索]按钮是否存在
        self.assertTrue(self.element_is_exist(".ivu-icon-search"))

        # 验证[添加]按钮是否存在
        self.assertTrue(self.element_is_exist(".mr10:nth-child(2) > span"))

        # 验证[上移]按钮是否存在
        self.assertTrue(self.element_is_exist(".mr10:nth-child(3) > span"))

        # 验证[下移]按钮是否存在
        self.assertTrue(self.element_is_exist(".mr10:nth-child(4) > span"))

        # 验证[删除]按钮是否存在
        self.assertTrue(self.element_is_exist(".mr10:nth-child(5) > span"))

        # 验证[修改]按是否存在
        self.assertTrue(self.element_is_exist(".ivu-btn:nth-child(6)"))

    def test_add_parent_menu(self):
        """[菜单管理]--新增一级菜单"""
        platform_api.open_page(self, 1, "菜单管理")

        # 新增一个一级菜单
        self.add_menu("测试菜单")

        # 验证菜单是否新增成功
        self.sleep(2)
        elements = self.get_elements("xpath=>//tr[@parenttr='Root']")
        menus = []
        for i in range(1, len(elements)+1):
            menus.append(self.get_text(f"xpath=>(//tr[@parenttr='Root'])[{i}]/td/div/span[2]"))
        self.assertIn("测试菜单", menus)

        # 清除测试数据，并刷新
        self.sleep(2)
        self.del_menu("测试菜单")

    def test_update_menu(self):
        """[菜单管理]--修改一级菜单"""
        platform_api.open_page(self, 1, "菜单管理")

        # 先新增一个菜单
        self.add_menu("测试菜单改")

        # 修改新增的菜单
        self.sleep(2)
        self.click("xpath=>//span[contains(.,'测试菜单改')]")
        self.click(".ivu-btn:nth-child(6)")
        self.sleep(1)
        self.clear("xpath=>(//input[@type='text'])[10]")
        self.type("xpath=>(//input[@type='text'])[10]", "测试菜单A")
        self.click(".menuMgt-model:nth-child(5) .ivu-btn:nth-child(1) > span")

        # 验证菜单是否修改成功
        self.sleep(2)
        elements = self.get_elements("xpath=>//tr[@parenttr='Root']")
        menus = []
        for i in range(1, len(elements) + 1):
            menus.append(self.get_text(f"xpath=>(//tr[@parenttr='Root'])[{i}]/td/div/span[2]"))
        self.assertIn("测试菜单A", menus)

        # 清除测试数据，并刷新
        self.sleep(2)
        self.del_menu("测试菜单A")

    def test_add_second_menu(self):
        """[菜单管理]--新增一个二级菜单"""
        platform_api.open_page(self, 1, "菜单管理")

        # 先新增一个一级菜单
        self.add_menu("测试菜单子")

        # 新增一个二级菜单
        self.sleep(2)
        self.click("xpath=>//span[contains(.,'测试菜单子')]")
        self.click(".mr10:nth-child(2) > span")
        self.sleep(1)
        self.clear("xpath=>(//input[@type='text'])[6]")
        self.type("xpath=>(//input[@type='text'])[6]", "二级菜单")
        self.sleep(2)
        self.click(".menuMgt-model:nth-child(4) .ivu-btn-primary")

        # 验证新增二级菜单是否成功
        text = self.get_text(".ivu-message .ivu-message-success >span")
        self.assertEqual(text, "添加成功")

        # 清除测试数据，并刷新
        self.sleep(2)
        self.del_menu("测试菜单子")

    def test_up_menu(self):
        """[菜单管理]--上移菜单"""
        platform_api.open_page(self, 1, "菜单管理")

        # 新增两个菜单，以便操作上移
        self.add_menu("测试菜单上1")
        self.sleep(1)
        self.add_menu("测试菜单上2")

        # 上移测试菜单上2
        self.sleep(3)
        self.click("xpath=>//span[contains(.,'测试菜单上2')]")
        self.click(".mr10:nth-child(3) > span")

        # 验证菜单是否下移成功
        text = self.get_text(".ivu-message .ivu-message-success >span")
        self.assertEqual(text, "移动成功")

        self.sleep(2)
        self.del_menu("测试菜单上1")
        self.del_menu("测试菜单上2")

    def test_down_menu(self):
        """[菜单管理]--下移菜单"""
        platform_api.open_page(self, 1, "菜单管理")

        # 新增两个菜单，以便操作下移
        self.add_menu("测试菜单下1")
        self.sleep(1)
        self.add_menu("测试菜单下2")

        # 下移测试菜单1
        self.sleep(3)
        self.click("xpath=>//span[contains(.,'测试菜单下1')]")
        self.click(".mr10:nth-child(4) > span")

        # 验证菜单是否下移成功
        text = self.get_text(".ivu-message .ivu-message-success >span")
        self.assertEqual(text, "移动成功")

        self.sleep(2)
        self.del_menu("测试菜单下2")
        self.del_menu("测试菜单下1")

    def test_del_menu(self):
        """[菜单管理]--删除一个菜单"""
        platform_api.open_page(self, 1, "菜单管理")

        # 先新增一个菜单
        self.add_menu("测试菜单删")

        # 删除菜单
        self.sleep(2)
        self.del_menu("测试菜单删")

        # 验证菜单是否删除成功
        self.sleep(1)
        elements = self.get_elements("xpath=>//tr[@parenttr='Root']")
        menus = []
        for i in range(1, len(elements)+1):
            menus.append(self.get_text(f"xpath=>(//tr[@parenttr='Root'])[{i}]/td/div/span[2]"))

        self.assertNotIn("测试菜单删", menus)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    TestRunner().debug()
