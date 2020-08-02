"""
用例作者：scf
用例明细：
    test_open_logo_manage(self):[logo管理]--验证logo管理页面回显信息
    test_modify_plat_homepage(self):[logo管理]--修改管理平台的首页文案
    test_modify_quality_homepage(self):[logo管理]--修改业务系统的首页文案
"""

from selenium_lib import Pyse, TestCase, TestRunner
from testcase.common import platform_api


class Test_Logo_Manage(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = Pyse("chrome")
        platform_api.login_platform(cls.driver)

    def test_open_logo_manage(self):
        """[logo管理]--验证logo管理页面回显信息"""
        platform_api.open_page(self, 1, "logo管理")

        # 验证管理平台上传按钮是否存在
        self.assertTrue(self.element_is_exist(".left-content span"))

        # 验证管理平台文案输入框是否存在
        self.assertTrue(self.element_is_exist(".left-content .el-input__inner"))

        # 验证业务系统上传按钮是否存在
        self.assertTrue(self.element_is_exist(".right-content span"))

        # 验证业务系统文案输入框是否存在
        self.assertTrue(self.element_is_exist(".right-content .el-input__inner"))

        # 验证保存按钮是否存在
        self.assertTrue(self.element_is_exist("div:nth-child(2) > .el-button"))

    def test_modify_plat_homepage(self):
        """[logo管理]--修改管理平台的首页文案"""
        platform_api.open_page(self, 1, "logo管理")

        # 修改文案
        self.clear(".left-content .el-input__inner")
        self.type(".left-content .el-input__inner", "技术开发平台")
        self.click("div:nth-child(2) > .el-button")

        # 验证文案修改是否成功
        self.sleep(1)
        text = self.get_attribute(".left-content .el-input__inner", "value")
        self.assertEqual("技术开发平台", text)

        # 还原文案内容
        self.sleep(2)
        self.clear(".left-content .el-input__inner")
        self.type(".left-content .el-input__inner", "Utry技术开发平台")
        self.click("div:nth-child(2) > .el-button")

    def test_modify_quality_homepage(self):
        """[logo管理]--修改业务系统的首页文案"""
        platform_api.open_page(self, 1, "logo管理")

        # 修改文案
        self.clear(".right-content .el-input__inner")
        self.type(".right-content .el-input__inner", "欢迎登陆质检分析系统")
        self.click("div:nth-child(2) > .el-button")

        # 验证文案修改是否成功
        self.sleep(1)
        text = self.get_attribute(".right-content .el-input__inner", "value")
        self.assertEqual("欢迎登陆质检分析系统", text)

        # 还原文案内容
        self.sleep(2)
        self.clear(".right-content .el-input__inner")
        self.type(".right-content .el-input__inner", "智能质检分析系统")
        self.click("div:nth-child(2) > .el-button")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    TestRunner().debug()
