"""
用例作者：scf
用例明细：
    test_platform_login(self):技术开发平台登录测试
    test_platform_exit(self):技术开发平登出测试
"""

from selenium_lib import Pyse, TestCase, TestRunner
from testcase.common import platform_api


class Test_PlatForm(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = Pyse("chrome")
        platform_api.login_platform(cls.driver)

    def test_platform_alogin(self):
        """Platform登录测试"""
        self.sleep(2)

        # 验证登录是否成功
        self.assertUrl(f"http://{platform_api.plat_ip}/#/")

    def test_platform_exit(self):
        """Platform登出测试"""
        platform_api.exit_platform(self)
        self.sleep(2)

        # 验证登出是否成功
        self.assertUrl(f"http://{platform_api.plat_ip}/#/login")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    TestRunner().debug()
