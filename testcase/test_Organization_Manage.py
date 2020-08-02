"""
用例作者：scf
用例明细：
    test_open_organization_manage(self):[组织管理]--验证组织管理页面回显信息
    test_add_organization(self):[组织管理]--新增一个组织
    test_del_organization(self):[组织管理]--删除一个组织
    test_update_organization(self):[组织管理]--修改一个组织
    test_add_child_organization(self):[组织管理]--新增一个子组织
    test_view_organization(self):[组织管理]--查看一个组织信息
    test_update_organization_cache(self):[组织管理]--更新组织缓存
"""

from selenium_lib import Pyse, TestCase, TestRunner
from testcase.common import platform_api


class Test_Organization_Manage(TestCase):
    def add_organization(self, org_name, org_code):
        """新增一个组织"""
        self.click(".mr10:nth-child(6) > span")
        self.sleep(1)
        self.clear("xpath=>(//input[@type='text'])[4]")
        self.type("xpath=>(//input[@type='text'])[4]", org_name)
        self.clear("xpath=>(//input[@type='text'])[5]")
        self.type("xpath=>(//input[@type='text'])[5]", org_code)
        self.click(".dpt-model:nth-child(3) .ivu-btn-primary > span")

    def del_organization(self, org_name):
        """删除一个组织"""
        self.click(f"xpath=>//span[contains(.,'{org_name}')]")
        self.click(".mr10:nth-child(3) > span")
        self.sleep(1)
        self.click(".tenant-model:nth-child(5) .ivu-btn-primary > span")
        self.sleep(2)

    @classmethod
    def setUpClass(cls):
        cls.driver = Pyse("chrome")
        cls.driver.maximize_window()
        platform_api.login_platform(cls.driver)

    def test_open_organization_manage(self):
        """[组织管理]--验证组织管理页面回显信息"""
        platform_api.open_page(self, 2, "组织管理")

        # 验证[搜索]输入框是否存在
        self.assertTrue(self.element_is_exist(".search .ivu-input"))

        # 验证[搜索]按钮是否存在
        self.assertTrue(self.element_is_exist(".ivu-icon-search"))

        # 验证[查看]按钮是否存在
        self.assertTrue(self.element_is_exist(".mr10:nth-child(2)"))

        # 验证[删除]按钮是否存在
        self.assertTrue(self.element_is_exist(".mr10:nth-child(3)"))

        # 验证[更新缓存]按钮是否存在
        self.assertTrue(self.element_is_exist(".mr10:nth-child(4)"))

        # 验证[修改]按钮是否存在
        self.assertTrue(self.element_is_exist(".mr10:nth-child(5)"))

        # 验证[新增]按钮是否存在
        self.assertTrue(self.element_is_exist(".mr10:nth-child(6)"))

    def test_add_organization(self):
        """[组织管理]--新增一个组织"""
        platform_api.open_page(self, 2, "组织管理")

        # 新增一个组织
        self.add_organization("测试新增组织", "120001")

        # 验证新增组织是否成功
        self.sleep(1)
        text = []
        num = len(self.get_elements("xpath=>//tr[@parenttr='Root']"))
        for i in range(1, num+1):
            org_name = self.get_text(f"xpath=>(//tr[@parenttr='Root']/td/div/span[2])[{i}]")
            text.append(org_name)
        self.assertIn("测试新增组织", text)

        # 清除测试数据
        self.sleep(1)
        self.del_organization("测试新增组织")

    def test_del_organization(self):
        """[组织管理]--删除一个组织"""
        platform_api.open_page(self, 2, "组织管理")

        # 先新增一个组织
        self.add_organization("测试删除组织", "120002")

        # 再删除新增的组织
        self.sleep(1)
        self.del_organization("测试删除组织")

        # 验证删除组织是否成功
        self.sleep(1)
        text = []
        num = len(self.get_elements("xpath=>//tr[@parenttr='Root']"))
        for i in range(1, num + 1):
            org_name = self.get_text(f"xpath=>(//tr[@parenttr='Root']/td/div/span[2])[{i}]")
            text.append(org_name)
        self.assertNotIn("测试删除组织", text)

    def test_update_organization(self):
        """[组织管理]--修改一个组织"""
        platform_api.open_page(self, 2, "组织管理")

        # 先新增一个组织
        self.add_organization("测试修改组织", "120013")

        # 修改组织
        self.sleep(2)
        self.click("xpath=>//span[contains(.,'测试修改组织')]")
        self.click(".mr10:nth-child(5)")
        self.sleep(2)
        self.clear("xpath=>(//input[@type='text'])[6]")
        self.type("xpath=>(//input[@type='text'])[6]", "测试组织改")
        self.click(".dpt-model:nth-child(4) .ivu-btn-primary > span")

        # 验证修改组织是否成功
        self.sleep(2)
        text = []
        num = len(self.get_elements("xpath=>//tr[@parenttr='Root']"))
        for i in range(1, num + 1):
            org_name = self.get_text(f"xpath=>(//tr[@parenttr='Root']/td/div/span[2])[{i}]")
            text.append(org_name)
        self.assertIn("测试组织改", text)

        # 清除测试数据
        self.sleep(2)
        self.del_organization("测试组织改")

    def test_add_child_organization(self):
        """[组织管理]--新增一个子组织"""
        platform_api.open_page(self, 2, "组织管理")

        # 先新增一个组织
        self.add_organization("测试建子组织", "120004")

        # 新增一个子组织
        self.sleep(1)
        self.click("xpath=>//span[contains(.,'测试建子组织')]")
        self.add_organization("子组织", "121001")

        # 验证新增子组织是否成功
        self.sleep(1)
        text = []
        num = len(self.get_elements("xpath=>//tr[not(@parenttr='Root') and (@class='ut-table-tree-leaf')]"))
        for i in range(1, num + 1):
            org_name = self.get_text(f"xpath=>(//tr[not(@parenttr='Root') and (@class='ut-table-tree-leaf')]/td/div/span[3])[{i}]")
            text.append(org_name)
        self.assertIn("子组织", text)

        # 清除测试数据
        self.sleep(1)
        self.click("xpath=>//span[3]")
        self.click(".mr10:nth-child(3) > span")
        self.sleep(1)
        self.click(".tenant-model:nth-child(5) .ivu-btn-primary > span")
        self.sleep(1)
        self.del_organization("测试建子组织")

    def test_view_organization(self):
        """[组织管理]--查看一个组织信息"""
        platform_api.open_page(self, 2, "组织管理")

        # 先新增一个组织
        self.add_organization("测试查看组织", "120005")

        # 查看,并验证新增组织信息是否正确
        self.sleep(1)
        self.click("xpath=>//span[contains(.,'测试查看组织')]")
        self.click(".mr10:nth-child(2)")
        self.sleep(2)
        org_name = self.get_attribute("xpath=>(//input[@type='text'])[2]", "value")
        org_code = self.get_attribute("xpath=>(//input[@type='text'])[3]", "value")
        self.assertEqual("测试查看组织", org_name)
        self.assertEqual("120005", org_code)

        self.sleep(1)
        self.click(".dpt-model:nth-child(2) span")

        # 清除测试数据
        self.sleep(1)
        self.click("xpath=>//span[contains(.,'测试查看组织')]")
        self.del_organization("测试查看组织")

    def test_update_organization_cache(self):
        """[组织管理]--更新组织缓存"""
        platform_api.open_page(self, 2, "组织管理")

        # 更新组织缓存
        self.click(".mr10:nth-child(4) > span")
        self.sleep(1)
        self.click(".tenant-model:nth-child(6) .ivu-btn-primary > span")

        # 验证更新缓存是否成功
        text = self.get_text(".ivu-message .ivu-message-success >span")
        self.assertEqual(text, "组织缓存刷新成功！")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    TestRunner().debug()
