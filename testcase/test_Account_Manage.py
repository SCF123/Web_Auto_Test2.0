"""
用例作者：scf
用例明细：
    test_open_account_manage(self):[账号管理]--验证账号管理页面回显信息
    test_add_account(self):[账号管理]--新增一个账号
    test_reset_password(self):[账号管理]--重置账户密码
    test_view_account(self):[账号管理]--查看账号，验证账号回显信息
    test_update_account(self):[账号管理]--修改账号
    test_query_by_account(self):[账号管理]--根据账号名称查询账号信息
    test_batch_update_account(self):[账号管理]--批量修改账号属性
"""

from selenium_lib import Pyse, TestCase, TestRunner
from testcase.common import platform_api


class Test_Account_Manage(TestCase):
    def add_account(self, account_name, account_code):
        """新增一个账号"""
        self.click("xpath=>//span[contains(.,'账号测试组织')]")
        self.click(".mt16 > span")
        self.sleep(1)
        self.clear("xpath=>(//input[@type='text'])[5]")
        self.type("xpath=>(//input[@type='text'])[5]", account_name)
        self.clear("xpath=>(//input[@type='text'])[6]")
        self.type("xpath=>(//input[@type='text'])[6]", account_code)
        # 勾选组织 账号测试组织
        org_elements = self.get_elements(".ivu-row:nth-child(3) > .ivu-col:nth-child(1) .ivu-tree > .ivu-tree-children")
        for i in range(2, len(org_elements) + 2):
            org_name = self.get_text(
                f".ivu-row:nth-child(3) > .ivu-col:nth-child(1) .ivu-tree > "
                f".ivu-tree-children:nth-child({i}) .ivu-tree-listItem .ivu-tree-title"
            )
            if "账号测试组织" == org_name:
                self.click(
                    f".ivu-row:nth-child(3) > .ivu-col:nth-child(1) .ivu-tree > "
                    f".ivu-tree-children:nth-child({i}) .ivu-tree-listItem .ivu-checkbox-input"
                )
                break

        # 勾选角色 账号测试角色
        role_elements = self.get_elements(
            ".ivu-row:nth-child(3) > .ivu-col:nth-child(2) .ivu-tree > .ivu-tree-children")
        for i in range(2, len(role_elements) + 2):
            role_name = self.get_text(
                f".ivu-row:nth-child(3) > .ivu-col:nth-child(2) .ivu-tree > "
                f".ivu-tree-children:nth-child({i}) .ivu-tree-listItem .ivu-tree-title"
            )
            if "账号测试角色" == role_name:
                self.click(
                    f".ivu-row:nth-child(3) > .ivu-col:nth-child(2) .ivu-tree > "
                    f".ivu-tree-children:nth-child({i}) .ivu-tree-listItem .ivu-checkbox-input"
                )
                break
        # 确定提交
        self.click(".item-break-all:nth-child(6) .ivu-btn:nth-child(2) > span")

    def del_account(self, ac_name):
        """删除一个账号"""
        num_1 = len(self.get_elements("#tr_Root_undefined"))
        for i in range(1, num_1 + 1):
            account_name = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/span)[{i}]")
            if ac_name == account_name:
                self.click(f"#tr_Root_undefined:nth-child({i}) .ivu-checkbox-input")
                break
        self.click(".ml0:nth-child(2) > span")
        self.sleep(2)
        self.click(".act-container > div:nth-child(3) .ivu-btn:nth-child(1) > span")
        # 对偶现的删除失败进行处理
        if "删除成功！" != self.get_text(".ivu-message span"):
            self.F5()
            platform_api.open_page(self, 2, "账号管理")
            num_2 = len(self.get_elements("#tr_Root_undefined"))
            for i in range(1, num_2 + 1):
                account_name = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/span)[{i}]")
                if ac_name == account_name:
                    self.click(f"#tr_Root_undefined:nth-child({i}) .ivu-checkbox-input")
                    break
            self.click(".ml0:nth-child(2) > span")
            self.sleep(2)
            self.click(".act-container > div:nth-child(3) .ivu-btn:nth-child(1) > span")
        self.sleep(1)

    @classmethod
    def setUpClass(cls):
        cls.driver = Pyse("chrome")
        platform_api.login_platform(cls.driver)

    def test_open_account_manage(self):
        """[账号管理]--验证账号管理页面回显信息"""
        platform_api.open_page(self, 2, "账号管理")

        # 验证[按组织搜索输入框]是否存在
        self.assertTrue(self.element_is_exist(".search .ivu-input"))

        # 验证[按组织搜索的搜索按钮]是否存在
        self.assertTrue(self.element_is_exist(".search .ivu-icon"))

        # 验证[新增账号]按钮是否存在
        self.assertTrue(self.element_is_exist(".mt16 > span"))

        # 验证[批量修改]按钮是否存在
        self.assertTrue(self.element_is_exist(".ml0:nth-child(4) > span"))

        # 验证[导入]按钮是否存在
        self.assertTrue(self.element_is_exist(".ml10:nth-child(6) > span"))

        # 验证[按账号搜索输入框]是否存在
        self.assertTrue(self.element_is_exist(".act-head .ivu-input"))

        # 验证[按账号搜索的搜索按钮]是否存在
        self.assertTrue(self.element_is_exist(".act-head .ivu-icon"))

    def test_add_account(self):
        """[账号管理]--新增一个账号"""

        # 先进入[人员管理]-[组织管理]页面创建一个测试组织
        platform_api.open_page(self, 2, "组织管理")
        # 新建一个组织
        self.click(".mr10:nth-child(6) > span")
        self.sleep(1)
        self.clear("xpath=>(//input[@type='text'])[4]")
        self.type("xpath=>(//input[@type='text'])[4]", "账号测试组织")
        self.clear("xpath=>(//input[@type='text'])[5]")
        self.type("xpath=>(//input[@type='text'])[5]", "900101")
        self.click(".dpt-model:nth-child(3) .ivu-btn-primary > span")
        # 关闭组织管理页面
        self.move_to_element(".icon-chuyidong")
        self.click(".icon-shibai")

        # 再进入[人员管理]-[角色管理]页面创建一个测试角色
        platform_api.open_page(self, 2, "角色管理")
        # 新建一个测试角色
        self.click(".float > span")
        self.clear("xpath=>//input[@type='text']")
        self.type("xpath=>//input[@type='text']", "账号测试角色")
        self.click(".role-left > div:nth-child(3) .ivu-btn:nth-child(1) > span")
        # 关闭角色管理页面
        self.move_to_element(".icon-chuyidong")
        self.click(".icon-shibai")

        # 最后进入[人员管理]-[账号管理]页面创建一个测试账号
        platform_api.open_page(self, 2, "账号管理")
        self.add_account("账号测试1", "test1")

        # 验证新增账号是否成功
        self.sleep(1)
        self.click("xpath=>//span[contains(.,'账号测试组织')]")
        self.sleep(1)
        accounts = []
        num = len(self.get_elements("#tr_Root_undefined"))
        for i in range(1, num + 1):
            account_name = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/span)[{i}]")
            accounts.append(account_name)
        self.assertIn("账号测试1", accounts)

        # 清除账号数据，保留创建的测试组织和角色，以便后续使用
        self.sleep(1)
        # self.del_account("账号测试1")
        num_1 = len(self.get_elements("#tr_Root_undefined"))
        for i in range(1, num_1 + 1):
            account_name = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/span)[{i}]")
            if "账号测试1" == account_name:
                self.click(f"#tr_Root_undefined:nth-child({i}) .ivu-checkbox-input")
                break
        self.click(".ml0:nth-child(2) > span")
        self.sleep(2)
        self.click(".act-container > div:nth-child(3) .ivu-btn:nth-child(1) > span")
        # 对偶现的删除失败进行处理
        if "删除成功！" != self.get_text(".ivu-message span"):
            self.F5()
            platform_api.open_page(self, 2, "账号管理")
            num_2 = len(self.get_elements("#tr_Root_undefined"))
            for i in range(1, num_2 + 1):
                account_name = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/span)[{i}]")
                if "账号测试1" == account_name:
                    self.click(f"#tr_Root_undefined:nth-child({i}) .ivu-checkbox-input")
                    break
            self.click(".ml0:nth-child(2) > span")
            self.sleep(2)
            self.click(".act-container > div:nth-child(3) .ivu-btn:nth-child(1) > span")
        self.sleep(1)

    def test_reset_password(self):
        """[账号管理]--重置账户密码"""
        platform_api.open_page(self, 2, "账号管理")

        # 新建一个测试账号
        self.add_account("账号测试2", "test2")

        # 重置新建账号的密码
        self.sleep(2)
        self.click("xpath=>//span[contains(.,'账号测试组织')]")
        num_1 = len(self.get_elements("#tr_Root_undefined"))
        for i in range(1, num_1 + 1):
            account_name = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/span)[{i}]")
            if "账号测试2" == account_name:
                self.click(f"#tr_Root_undefined:nth-child({i}) .ivu-checkbox-input")
                break
        self.click(".mr10 > span")
        self.sleep(1)
        self.click("div:nth-child(4) .ivu-btn-primary > span")

        # 验证密码重置是否成功
        text = self.get_text(".ivu-message span")
        self.assertEqual(text, "重置密码成功！")

        # 清除测试账号
        self.sleep(1)
        self.click(".ml0:nth-child(2) > span")
        self.sleep(2)
        self.click(".act-container > div:nth-child(3) .ivu-btn:nth-child(1) > span")
        # 对偶现的删除失败进行处理
        if "删除成功！" != self.get_text(".ivu-message span"):
            self.F5()
            platform_api.open_page(self, 2, "账号管理")
            num_2 = len(self.get_elements("#tr_Root_undefined"))
            for i in range(1, num_2 + 1):
                account_name = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/span)[{i}]")
                if "账号测试1" == account_name:
                    self.click(f"#tr_Root_undefined:nth-child({i}) .ivu-checkbox-input")
                    break
            self.click(".ml0:nth-child(2) > span")
            self.sleep(2)
            self.click(".act-container > div:nth-child(3) .ivu-btn:nth-child(1) > span")
        self.sleep(1)

    def test_update_account(self):
        """[账号管理]--修改账号"""
        platform_api.open_page(self, 2, "账号管理")

        # 新建一个测试账号
        self.add_account("账号测试4", "test4")

        # 修改账号
        self.sleep(2)
        self.click("xpath=>//span[contains(.,'账号测试组织')]")
        num_1 = len(self.get_elements("#tr_Root_undefined"))
        for i in range(1, num_1 + 1):
            account_name = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/span)[{i}]")
            if "账号测试4" == account_name:
                self.click(f"#tr_Root_undefined:nth-child({i}) .ivu-checkbox-input")
                break
        self.click(".mar0 > span")
        self.clear("div:nth-child(1) > .addForm .ivu-col:nth-child(1) .ivu-input")
        self.type("div:nth-child(1) > .addForm .ivu-col:nth-child(1) .ivu-input", "账号测试4改")
        self.click(".item-break-all:nth-child(7) .ivu-btn-primary > span")

        # 验证账号修改是否成功
        self.sleep(2)
        self.click("xpath=>//span[contains(.,'账号测试组织')]")
        names = []
        for i in range(1, num_1 + 1):
            account_name = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/span)[{i}]")
            names.append(account_name)
        self.assertIn("账号测试4改", names)

        # 清除测试账号
        self.sleep(1)
        self.del_account("账号测试4改")

    def test_query_by_account(self):
        """[账号管理]--根据账号名称查询账号信息"""
        platform_api.open_page(self, 2, "账号管理")

        # 新建一个测试账号
        self.add_account("账号测试5", "test5")

        # 查询新建的账号
        self.sleep(1)
        self.clear(".act-head .ivu-input")
        self.type(".act-head .ivu-input", "账号测试5")
        self.click(".act-head .ivu-icon")

        # 验证查询结果是否正确
        account_name = self.get_text(f"xpath=>//tr[@id='tr_Root_undefined']/td[2]/div/span")
        self.assertEqual("账号测试5", account_name)

        # 清除测试账号
        self.sleep(1)
        self.del_account("账号测试5")

    def test_batch_update_account(self):
        """[账号管理]--批量修改账号属性"""
        platform_api.open_page(self, 2, "账号管理")

        # 新建两个测试账号
        self.add_account("账号测试6", "test6")
        self.sleep(2)
        self.add_account("账号测试7", "test7")

        # 选中这两个新建的账号进行修改
        self.sleep(2)
        self.click("xpath=>//span[contains(.,'账号测试组织')]")
        self.click("thead .ivu-checkbox-input")
        self.click(".ml0:nth-child(4) > span")
        self.click("td > .ivu-checkbox-wrapper .ivu-checkbox-input")
        self.click(".batch-update .ivu-btn-primary > span")

        # 验证批量修改是否成功
        text = self.get_text(".el-message > p")
        self.assertEqual(text, "批量修改成功！")

        # 清除测试账号
        self.sleep(1)
        self.clear(".act-head .ivu-input")
        self.type(".act-head .ivu-input", "账号测试6")
        self.click(".act-head .ivu-icon")
        self.del_account("账号测试6")
        self.clear(".act-head .ivu-input")
        self.type(".act-head .ivu-input", "账号测试7")
        self.click(".act-head .ivu-icon")
        self.del_account("账号测试7")

    def test_view_account(self):
        """[账号管理]--查看账号，验证账号回显信息"""
        platform_api.open_page(self, 2, "账号管理")

        # 新建一个测试账号
        self.add_account("账号测试3", "test3")

        # 选中新建的账号查看
        self.sleep(3)
        self.click("xpath=>//span[contains(.,'账号测试组织')]")
        num_1 = len(self.get_elements("#tr_Root_undefined"))
        for i in range(1, num_1 + 1):
            account_name = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/span)[{i}]")
            if "账号测试3" == account_name:
                self.click(f"#tr_Root_undefined:nth-child({i}) .ivu-checkbox-input")
                break
        self.click(".ml0:nth-child(7) > span")

        # 验证账号姓名是否正确
        user_name = self.get_attribute(".ivu-col:nth-child(1) .ivu-input-disabled", "value")
        self.assertEqual("账号测试3", user_name)
        # 验证账号是否正确
        user_code = self.get_attribute(".ivu-col:nth-child(2) .ivu-input-disabled", "value")
        self.assertEqual("test3", user_code)
        # 验证勾选的组织是否正确
        checked = "ivu-checkbox ivu-checkbox-checked ivu-checkbox-disabled"
        org_elements = self.get_elements(
            ".ivu-modal-body:nth-child(2) .ivu-row:nth-child(2) > .ivu-col:nth-child(1) .ivu-tree > .ivu-tree-children"
        )
        for i in range(1, len(org_elements) + 1):
            org_name = self.get_text(
                f".ivu-modal-body:nth-child(2) .ivu-row:nth-child(2) > .ivu-col:nth-child(1) "
                f".ivu-tree > .ivu-tree-children:nth-child({i}) .ivu-tree-title"
            )
            if "账号测试组织" == org_name:
                org_attr = self.get_attribute(
                    f".ivu-modal-body:nth-child(2) .ivu-row:nth-child(2) > .ivu-col:nth-child(1) "
                    f".ivu-tree > .ivu-tree-children:nth-child({i}) .ivu-checkbox-disabled",
                    "class"
                )
                self.assertEqual(checked, org_attr)
                break
        # 验证勾选的角色是否正确
        role_elements = self.get_elements(
            ".ivu-modal-body:nth-child(2) > .addForm:nth-child(1) > "
            ".ivu-row:nth-child(2) > .ivu-col:nth-child(2) .ivu-tree-children"
        )
        for i in range(1, len(role_elements) + 1):
            role_name = self.get_text(
                f".ivu-modal-body:nth-child(2) > .addForm:nth-child(1) > .ivu-row:nth-child(2) > "
                f".ivu-col:nth-child(2) .ivu-tree-children:nth-child({i}) .ivu-tree-title"
            )
            if "账号测试角色" == role_name:
                role_attr = self.get_attribute(
                    f".ivu-modal-body:nth-child(2) > .addForm:nth-child(1) > .ivu-row:nth-child(2) > "
                    f".ivu-col:nth-child(2) .ivu-tree > .ivu-tree-children:nth-child({i}) .ivu-checkbox-disabled",
                    "class"
                )
                self.assertEqual(checked, role_attr)
                break
        # 验证完之后，点击[取消]按钮返回列表页
        self.click(".item-break-all:nth-child(9) .ivu-btn-ghost > span")

        # 清除测试账号
        self.sleep(1)
        self.click(".ml0:nth-child(2) > span")
        self.sleep(2)
        self.click(".act-container > div:nth-child(3) .ivu-btn:nth-child(1) > span")
        # 对偶现的删除失败进行处理
        if "删除成功！" != self.get_text(".ivu-message span"):
            self.F5()
            platform_api.open_page(self, 2, "账号管理")
            num_2 = len(self.get_elements("#tr_Root_undefined"))
            for i in range(1, num_2 + 1):
                account_name = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/span)[{i}]")
                if "账号测试3" == account_name:
                    self.click(f"#tr_Root_undefined:nth-child({i}) .ivu-checkbox-input")
                    break
            self.click(".ml0:nth-child(2) > span")
            self.sleep(2)
            self.click(".act-container > div:nth-child(3) .ivu-btn:nth-child(1) > span")
        self.sleep(2)

        # 清除账号的测试角色
        platform_api.open_page(self, 2, "角色管理")
        self.click("xpath=>//span[contains(.,'账号测试角色')]")
        self.click(".role_btn > .del-btn > .icon")
        self.sleep(1)
        self.click("div:nth-child(5) .ivu-btn-primary > span")
        self.sleep(5)

        # 清除账号的测试组织
        platform_api.open_page(self, 2, "组织管理")
        self.click("xpath=>//span[contains(.,'账号测试组织')]")
        self.click(".mr10:nth-child(3) > span")
        self.sleep(1)
        self.click(".tenant-model:nth-child(5) .ivu-btn-primary > span")
        self.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    TestRunner().debug()
