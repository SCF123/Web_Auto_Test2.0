"""
用例作者：scf
用例明细：
    test_open_personal_info(self):[个人信息]--验证个人信息页面回显信息
    test_update_personal_info(self):[个人信息]--修改个人信息
    test_update_personal_password(self):[个人信息]--修改账号密码
    test_open_inbox(self):[个人信息]--打开收件箱页面，验证回显信息
"""

from selenium_lib import Pyse, TestCase, TestRunner
from testcase.common import platform_api


class Test_Message_Service(TestCase):
    def open_personal_info(self):
        self.sleep(1)
        self.F5()
        self.click(".icon-message")
        self.sleep(1)

    @classmethod
    def setUpClass(cls):
        cls.driver = Pyse("chrome")
        platform_api.login_platform(cls.driver)

    def test_open_personal_info(self):
        """[个人信息]--验证个人信息页面回显信息"""
        self.open_personal_info()

        # 验证[账户名]是否正确
        name = self.get_text("tr:nth-child(1) > .pl")
        self.assertEqual(platform_api.plat_account, name)

        # 验证[修改信息]按钮是否存在
        self.assertTrue(self.element_is_exist(".left-top > .mr10 > span"))

        # 验证[修改密码]按钮是否存在
        self.assertTrue(self.element_is_exist(".left-top > .ivu-btn:nth-child(2) > span"))

        # 验证[消息状态]下拉选择框是否存在
        self.assertTrue(self.element_is_exist(".w200 .ivu-select-selected-value"))

        # 验证[发送时间]输入框是否存在
        self.assertTrue(self.element_is_exist(".ivu-col:nth-child(2) .ivu-date-picker-rel .ivu-input"))

        # 验证[消息标题]输入框是否存在
        self.assertTrue(self.element_is_exist(".ivu-row:nth-child(2) > .ivu-col:nth-child(1) .w200 > .ivu-input"))

        # 验证[消息来源]输入框是否存在
        self.assertTrue(self.element_is_exist(".ivu-row:nth-child(2) > .ivu-col:nth-child(2) .ivu-input"))

        # 验证[查询]按钮是否存在
        self.assertTrue(self.element_is_exist(".tb-InfoDiv:nth-child(2) .search .mr10 > span"))

        # 验证[重置]按钮是否存在
        self.assertTrue(self.element_is_exist(".tb-InfoDiv:nth-child(2) .search .ivu-btn:nth-child(2) > span"))

        # 验证[发消息]按钮是否存在
        self.assertTrue(self.element_is_exist(".tb-InfoDiv:nth-child(2) .ivu-btn-primary > span"))

        # 验证[回复]按钮是否存在
        self.assertTrue(self.element_is_exist(".tb-InfoDiv:nth-child(2) .mr10:nth-child(2) > span"))

        # 验证[标记未读]按钮是否存在
        self.assertTrue(self.element_is_exist(".mr10:nth-child(3) > span"))

        # 验证[标记已读]按钮是否存在
        self.assertTrue(self.element_is_exist(".mr10:nth-child(4) > span"))

        # 验证[删除]是否存在
        self.assertTrue(self.element_is_exist(".mr10:nth-child(5)"))

    def test_update_personal_info(self):
        """[个人信息]--修改个人信息"""
        self.open_personal_info()

        # 修改个人信息
        self.click(".left-top > .mr10 > span")
        self.sleep(1)
        self.click(".ivu-form-item:nth-child(3) > .ivu-form-item-content:nth-child(2) .ivu-icon-ios-arrow-down")
        self.click("xpath=>//li[contains(.,'女')]")
        self.clear(".ivu-form-item:nth-child(4) .ivu-input")
        self.type(".ivu-form-item:nth-child(4) .ivu-input", "18")
        self.click(".ivu-form-item:nth-child(5) .ivu-icon-ios-arrow-down")
        self.click("xpath=>//li[contains(.,'专科')]")
        self.sleep(1)
        self.click(".modModel .ivu-btn-primary")

        # 验证个人信息修改是否成功
        self.sleep(2)
        # 验证性别
        sex = self.get_text("tr:nth-child(3) > .pl")
        self.assertEqual("女", sex)
        # 验证年龄
        age = self.get_text("tr:nth-child(4) > .pl")
        self.assertEqual("18", age)
        # 验证学历
        edu = self.get_text("tr:nth-child(5) > .pl")
        self.assertEqual("专科", edu)

    def test_update_personal_password(self):
        """[个人信息]--修改账号密码"""
        self.open_personal_info()

        # 修改账号密码
        self.click(".left-top > .ivu-btn:nth-child(2) > span")
        self.sleep(1)
        self.type("xpath=>(//input[@type='password'])[4]", "123456")
        self.type("xpath=>(//input[@type='password'])[5]", "123456")
        self.type("xpath=>(//input[@type='password'])[6]", "123456")
        self.click(".pi-wrap > div:nth-child(3) .ivu-btn:nth-child(1) > span")

        # 验证密码修改是否成功
        text = self.get_text(".ivu-message span")
        self.assertEqual("修改密码成功！", text)

    def test_open_inbox(self):
        """[个人信息]--打开收件箱页面，验证回显信息"""
        self.click(".icon-message")
        self.sleep(1)

        # 打开收件箱
        self.click(".ivu-tabs-tab:nth-child(3) > span:nth-child(1)")

        # 验证[消息标题]输入框是否存在
        self.assertTrue(self.element_is_exist(".ivu-row:nth-child(1) > .ivu-col:nth-child(1) .ivu-input"))

        # 验证[收件人]输入框是否存在
        self.assertTrue(self.element_is_exist(".ivu-row:nth-child(1) > .ivu-col:nth-child(2) .w200 > .ivu-input"))

        # 验证[发送时间]输入框是否存在
        self.assertTrue(self.element_is_exist(".ivu-col:nth-child(1) .ivu-date-picker-rel .ivu-input"))

        # 验证[查询]按钮是否存在
        self.assertTrue(self.element_is_exist(".tb-InfoDiv:nth-child(1) .search .mr10 > span"))

        # 验证[重置]按钮是否存在
        self.assertTrue(self.element_is_exist(".tb-InfoDiv:nth-child(1) .search .ivu-btn:nth-child(2) > span"))

        # 验证[发消息]按钮是否存在
        self.assertTrue(self.element_is_exist(".tb-InfoDiv:nth-child(1) .ivu-btn-primary > span"))

        # 验证[删除]按钮是否存在
        self.assertTrue(self.element_is_exist(".tb-InfoDiv:nth-child(1) .btns .ivu-btn-ghost > span"))

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    TestRunner().debug()
