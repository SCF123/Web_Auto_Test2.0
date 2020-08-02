"""
用例作者：scf
用例明细：
    test_open_role_manage(self):[角色管理]--验证角色管理页面回显信息
    test_add_role(self):[角色管理]--新增一个角色
    test_del_role(self):[角色管理]--删除一个角色
    test_update_role(self):[角色管理]--修改一个角色
    test_role_bind_power(self):[角色管理]--给一个角色绑定权限
    test_role_revoke_power(self):[角色管理]--取消一个角色的权限
    test_role_batch_power(self):[角色管理]--给多个角色批量授权
"""

from selenium_lib import Pyse, TestCase, TestRunner
from testcase.common import platform_api


class Test_Role_Manage(TestCase):
    def add_role(self, role_name, role_dsc):
        """新增一个角色"""
        self.click(".float > span")
        self.clear("xpath=>//input[@type='text']")
        self.type("xpath=>//input[@type='text']", role_name)
        self.clear("xpath=>//textarea")
        self.type("xpath=>//textarea", role_dsc)
        self.click(".role-left > div:nth-child(3) .ivu-btn:nth-child(1) > span")

    def del_role(self, role_name):
        """删除一个角色"""
        self.click(f"xpath=>//span[contains(.,'{role_name}')]")
        self.click(".role_btn > .del-btn > .icon")
        self.sleep(1)
        self.click("div:nth-child(5) .ivu-btn-primary > span")
        self.sleep(3)

    @classmethod
    def setUpClass(cls):
        cls.driver = Pyse("chrome")
        cls.driver.maximize_window()
        platform_api.login_platform(cls.driver)

    def test_open_role_manage(self):
        """[角色管理]--验证角色管理页面回显信息"""
        platform_api.open_page(self, 2, "角色管理")

        # 验证[新增角色]按钮是否存在
        self.assertTrue(self.element_is_exist(".float > span"))

        # 验证[人员页签]是否存在
        self.assertTrue(self.element_is_exist("#tab-ctrl-two .ivu-tabs-tab:nth-child(2) > span:nth-child(1)"))

        # 验证[权限页签]是否存在
        self.assertTrue(self.element_is_exist("#tab-ctrl-two .ivu-tabs-tab:nth-child(3) > span:nth-child(1)"))

        # 验证[部门下拉选择框]是否存在
        self.assertTrue(self.element_is_exist("#search .tree-select .ivu-input"))

        # 验证[账号搜索输入框]是否存在
        self.assertTrue(self.element_is_exist("#search .search-con .ivu-input"))

        # 验证[账号搜索]按钮是否存在
        self.assertTrue(self.element_is_exist("#search .search-con .ivu-icon"))

    def test_add_role(self):
        """[角色管理]--新增一个角色"""
        platform_api.open_page(self, 2, "角色管理")

        # 新增一个角色
        self.add_role("角色测试1", "测试新增一个角色")

        # 验证新增角色是否成功
        self.sleep(2)
        elements = self.get_elements(".roleList > .roleBox")
        roles = []
        for i in range(1, len(elements)+1):
            role = self.get_text(f".roleList > .roleBox:nth-child({i}) > .role-div")
            roles.append(role)

        self.assertIn("角色测试1", roles)

        # 清除测试数据
        self.del_role("角色测试1")

    def test_del_role(self):
        """[角色管理]--删除一个角色"""
        platform_api.open_page(self, 2, "角色管理")

        # 先新建一个角色
        self.add_role("角色测试2", "测试删除一个角色")
        self.sleep(1)

        # 删除新建的角色
        self.del_role("角色测试2")

        # 验证删除角色是否成功
        elements = self.get_elements(".roleList > .roleBox")
        roles = []
        for i in range(1, len(elements) + 1):
            role = self.get_text(f".roleList > .roleBox:nth-child({i}) > .role-div")
            roles.append(role)

        self.assertNotIn("角色测试2", roles)

    def test_update_role(self):
        """[角色管理]--修改一个角色"""
        platform_api.open_page(self, 2, "角色管理")

        # 先新建一个角色
        self.add_role("角色测试3", "测试修改一个角色")
        self.sleep(1)

        # 修改角色
        self.click("xpath=>//span[contains(.,'角色测试3')]")
        self.click(".role_btn > .write-btn > .icon")
        self.clear("xpath=>(//input[@type='text'])[2]")
        self.type("xpath=>(//input[@type='text'])[2]", "角色测试3改")
        self.click("div:nth-child(4) .ivu-btn-primary")

        # 验证修改角色是否成功
        self.sleep(2)
        elements = self.get_elements(".roleList > .roleBox")
        roles = []
        for i in range(1, len(elements) + 1):
            role = self.get_text(f".roleList > .roleBox:nth-child({i}) > .role-div")
            roles.append(role)

        self.assertIn("角色测试3改", roles)

        # 清除测试数据
        self.del_role("角色测试3改")

    def test_role_bind_power(self):
        """[角色管理]--给一个角色绑定权限"""
        platform_api.open_page(self, 2, "角色管理")

        # 先新建一个角色
        self.add_role("角色测试4", "测试给角色绑定权限")
        self.sleep(1)

        # 给新建的角色绑定权限
        self.click("xpath=>//span[contains(.,'角色测试4')]")
        self.click(".ivu-tabs-tab:nth-child(5)")
        self.sleep(3)
        self.click(".ivu-tree-children:nth-child(1) .ivu-checkbox-input")
        self.click(".ivu-tabs-tabpane:nth-child(4) .ut-toolbar span")
        self.sleep(1)

        # 验证角色绑定权限是否成功
        text = self.get_text(".ivu-message .ivu-message-success >span")
        self.assertEqual(text, "绑定成功！")

        # 清除测试数据
        self.sleep(1)
        self.click("xpath=>//span[contains(.,'角色测试4')]")
        self.del_role("角色测试4")

    def test_role_revoke_power(self):
        """[角色管理]--取消一个角色的权限"""
        platform_api.open_page(self, 2, "角色管理")

        # 先新建一个角色，并绑定权限
        self.add_role("角色测试5", "测试取消角色权限")
        self.sleep(1)
        # 给角色绑定权限
        self.click("xpath=>//span[contains(.,'角色测试5')]")
        self.click(".ivu-tabs-tab:nth-child(5)")
        self.sleep(3)
        # 给角色绑定 系统管理 权限
        self.click(".ivu-tree-children:nth-child(1) .ivu-checkbox-input")
        self.click(".ivu-tabs-tabpane:nth-child(4) .ut-toolbar span")
        self.sleep(1)

        # 取消角色绑定的权限
        self.click(".ivu-tabs-tab:nth-child(4)")
        self.sleep(3)
        self.click(".ivu-tree-children:nth-child(1) .ivu-checkbox-input")
        self.click(".ivu-tabs-tabpane:nth-child(3) .ut-toolbar span")
        self.sleep(1)

        # 验证取消角色权限是否成功
        text = self.get_text(".ivu-message .ivu-message-success >span")
        self.assertEqual(text, "操作成功!")

        # 清除测试数据
        self.sleep(1)
        self.click("xpath=>//span[contains(.,'角色测试5')]")
        self.del_role("角色测试5")

    def test_role_batch_power(self):
        """[角色管理]--给多个角色批量授权"""
        platform_api.open_page(self, 2, "角色管理")

        # 新建两个角色
        self.add_role("角色测试6", "测试批量授权多个角色")
        self.sleep(1)
        self.add_role("角色测试7", "测试批量授权多个角色")
        self.sleep(1)

        # 给新建的两个角色授权
        self.click("xpath=>//span[contains(.,'角色测试6')]")
        self.click("xpath=>//span[contains(.,'角色测试7')]")
        self.click("#tab-ctrl-two .ivu-tabs-tab:nth-child(3) > span:nth-child(1)")
        self.sleep(3)
        self.click(".ivu-tabs-tabpane:nth-child(2) .ivu-tree-children:nth-child(1) .ivu-checkbox-input")
        self.click(".ivu-tabs-tabpane:nth-child(2) .ivu-tree:nth-child(1) > .ivu-tree-children:nth-child(2) .ivu-checkbox-input")
        self.click(".ml5")
        self.sleep(1)

        # 验证批量授权是否成功
        text = self.get_text(".ivu-message .ivu-message-success >span")
        self.assertEqual(text, "授权成功！")

        # 清除测试数据
        self.sleep(1)
        self.click("xpath=>//span[contains(.,'角色测试6')]")
        self.del_role("角色测试6")
        self.del_role("角色测试7")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    TestRunner().debug()
