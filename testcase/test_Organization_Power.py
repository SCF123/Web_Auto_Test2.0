"""
用例作者：scf
用例明细：
    test_open_data_power(self):[组织管理]--验证数据权限弹窗回显信息
    test_organization_bind_power(self):[组织管理]--给组织绑定数据权限
"""

from selenium_lib import Pyse, TestCase, TestRunner
from testcase.common import platform_api


class Test_Organization_Power(TestCase):
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
        platform_api.login_platform(cls.driver)

    def test_open_data_power(self):
        """[组织管理]--验证数据权限弹窗回显信息"""
        platform_api.open_page(self, 2, "组织管理")

        # 先新增一个组织
        self.add_organization("测试组织1", "120006")

        # 打开数据权限弹窗
        self.click("xpath=>//span[contains(.,'测试组织1')]")
        self.click(".ivu-btn:nth-child(7) > span")
        self.sleep(2)

        # 验证 数据范围下拉选择框中的数据是否正确
        site_menus = platform_api.get_site_menus()
        self.assertIsNotNone(site_menus)  # 验证一下接口是否获取到数据

        for i in range(1, len(site_menus)+1):
            self.click("xpath=>//i[2]")
            site = self.get_text(f".ivu-select-visible .ivu-select-item:nth-child({i})")
            self.assertTrue(site in site_menus)
            self.sleep(1)
            self.click(f".ivu-select-visible .ivu-select-item:nth-child({i})")
            site_pages = site_menus[site]
            for j in range(1, len(site_pages)+1):
                self.sleep(0.1)
                page = self.get_text(f".ivu-checkbox-wrapper:nth-child({j}) .tool-content")
                self.assertIn(page, site_pages)

        # 清除测试数据
        self.click(".dp-modal .ivu-btn:nth-child(2) > span")
        self.click(".mr10:nth-child(3) > span")
        self.sleep(1)
        self.click(".tenant-model:nth-child(5) .ivu-btn-primary > span")
        self.sleep(1)

    def test_organization_bind_power(self):
        """[组织管理]--给组织绑定数据权限"""
        platform_api.open_page(self, 2, "组织管理")

        # 新增一个测试组织
        self.add_organization("测试组织2", "120007")
        # 关闭组织管理页面
        self.move_to_element(".icon-chuyidong")
        self.click(".icon-shibai")

        # 进入[人员管理]-[角色管理]页面创建一个测试角色
        platform_api.open_page(self, 2, "角色管理")
        # 新建一个测试角色
        self.click(".float > span")
        self.clear("xpath=>//input[@type='text']")
        self.type("xpath=>//input[@type='text']", "测试角色")
        self.click(".role-left > div:nth-child(3) .ivu-btn:nth-child(1) > span")
        # 关闭角色管理页面
        self.move_to_element(".icon-chuyidong")
        self.click(".icon-shibai")

        # 进入[人员管理]-[账号管理]页面创建一个测试账号
        platform_api.open_page(self, 2, "账号管理")
        # 新建一个测试账号
        self.click("xpath=>//span[contains(.,'测试组织2')]")
        self.click(".mt16 > span")
        self.sleep(1)
        self.clear("xpath=>(//input[@type='text'])[5]")
        self.type("xpath=>(//input[@type='text'])[5]", "测试账号")
        self.clear("xpath=>(//input[@type='text'])[6]")
        self.type("xpath=>(//input[@type='text'])[6]", "testac")
        # 勾选组织 测试组织2
        org_elements = self.get_elements(".ivu-row:nth-child(3) > .ivu-col:nth-child(1) .ivu-tree > .ivu-tree-children")
        for i in range(2, len(org_elements)+2):
            org_name = self.get_text(
                f".ivu-row:nth-child(3) > .ivu-col:nth-child(1) .ivu-tree > "
                f".ivu-tree-children:nth-child({i}) .ivu-tree-listItem .ivu-tree-title"
            )
            if "测试组织2" == org_name:
                self.click(
                    f".ivu-row:nth-child(3) > .ivu-col:nth-child(1) .ivu-tree > "
                    f".ivu-tree-children:nth-child({i}) .ivu-tree-listItem .ivu-checkbox-input"
                )
                break

        # 勾选角色 测试角色
        role_elements = self.get_elements(".ivu-row:nth-child(3) > .ivu-col:nth-child(2) .ivu-tree > .ivu-tree-children")
        for i in range(2, len(role_elements)+2):
            role_name = self.get_text(
                f".ivu-row:nth-child(3) > .ivu-col:nth-child(2) .ivu-tree > "
                f".ivu-tree-children:nth-child({i}) .ivu-tree-listItem .ivu-tree-title"
            )
            if "测试角色" == role_name:
                self.click(
                    f".ivu-row:nth-child(3) > .ivu-col:nth-child(2) .ivu-tree > "
                    f".ivu-tree-children:nth-child({i}) .ivu-tree-listItem .ivu-checkbox-input"
                )
                break
        # 确定提交
        self.click(".item-break-all:nth-child(6) .ivu-btn:nth-child(2) > span")

        # 关闭账号管理页面
        self.move_to_element(".icon-chuyidong")
        self.click(".icon-shibai")

        # 最后回到组织管理页面，进行数据绑定操作
        self.sleep(2)
        platform_api.open_page(self, 2, "组织管理")

        # 打开数据权限弹窗
        self.click("xpath=>//span[contains(.,'测试组织2')]")
        self.click(".ivu-btn:nth-child(7) > span")
        self.sleep(2)
        self.click("xpath=>//i[2]")
        # 选择第二项：人员管理
        self.sleep(1)
        # 判断打开数据权限弹窗后，是否能够获取到数据权限信息，如果没有获取到，则关闭弹窗，重新打开
        if not self.element_is_exist(".ivu-select-visible .ivu-select-item"):
            self.click(".dp-modal .modal-close .icon")
            self.sleep(1)
            self.click(".ivu-btn:nth-child(7) > span")
            self.sleep(1)
            self.click("xpath=>//i[2]")
            self.sleep(1)

        self.click(f".ivu-select-visible .ivu-select-item:nth-child(2)")
        # 选择前两个复选框（页面功能）
        self.sleep(1)
        self.click(".ivu-checkbox-group-item:nth-child(1) .ivu-checkbox-input")
        self.click(".ivu-checkbox-wrapper:nth-child(2) .ivu-checkbox-input")
        # 选择对象  测试角色
        self.sleep(1)
        self.click(".ivu-select-multiple .ivu-icon-ios-arrow-down")
        self.click("xpath=>//li[contains(.,'测试角色')]")
        self.click(".ivu-select-visible .ivu-icon-ios-arrow-down")
        # 选择账号 测试账号
        self.sleep(1)
        self.click("#tr_Root_undefined .ivu-checkbox-input")
        self.sleep(1)
        self.click(".dp-modal .ivu-btn-primary > span")

        # 验证授权信息绑定是否成功
        text = self.get_text(".ivu-message .ivu-message-success >span")
        self.assertEqual(text, "保存授权信息成功")

        # 再次打开数据权限弹窗，进行权限修改
        self.sleep(2)
        self.click(".ivu-btn:nth-child(7) > span")
        self.sleep(1)
        self.click("xpath=>//i[2]")
        # 选择第二项：人员管理
        self.sleep(1)
        if not self.element_is_exist(".ivu-select-visible .ivu-select-item"):
            self.click(".dp-modal .ivu-btn:nth-child(2) > span")
            self.sleep(1)
            self.click(".ivu-btn:nth-child(7) > span")
            self.sleep(1)
            self.click("xpath=>//i[2]")
            self.sleep(1)
        self.click(f".ivu-select-visible .ivu-select-item:nth-child(2)")
        # 选择第一个复选框（页面功能）
        self.sleep(1)
        self.click(".ivu-checkbox-group-item:nth-child(1) .ivu-checkbox-input")
        self.sleep(1)
        self.click(".dp-modal .ivu-btn-primary > span")

        # 验证授权信息绑定修改是否成功
        text = self.get_text(".ivu-message .ivu-message-success >span")
        self.assertEqual(text, "保存授权信息成功")

        # 清除测试数据
        self.sleep(2)
        platform_api.open_page(self, 2, "账号管理")
        self.click("xpath=>//span[contains(.,'测试组织2')]")
        self.click("#tr_Root_undefined .ivu-checkbox-input")
        self.click(".ml0:nth-child(2) > span")
        self.click(".act-container > div:nth-child(3) .ivu-btn:nth-child(1) > span")
        # 关闭账号管理页面
        self.move_to_element(".icon-chuyidong")
        self.click(".icon-shibai")

        platform_api.open_page(self, 2, "角色管理")
        self.click("xpath=>//span[contains(.,'测试角色')]")
        self.click(".role_btn > .del-btn > .icon")
        self.sleep(3)
        self.click("div:nth-child(5) .ivu-btn-primary > span")
        self.sleep(3)
        # 关闭角色管理页面
        self.move_to_element(".icon-chuyidong")
        self.click(".icon-shibai")

        platform_api.open_page(self, 2, "组织管理")
        self.del_organization("测试组织2")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    TestRunner().debug()
