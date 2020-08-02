"""
用例作者：scf
用例明细：
    test_open_update_index(self):[系统管理]--[更新索引]，验证更新索引页面回显信息
    test_add_index(self):[系统管理]--[更新索引]，新增一个索引
    test_update_index(self):[系统管理]--[更新索引]，修改一个索引
    test_run_index(self):[系统管理]--[更新索引]，运行一个索引
    test_del_index(self):[系统管理]--[更新索引]，删除一个索引
"""

from selenium_lib import Pyse, TestCase, TestRunner
from testcase.common import platform_api


class Test_Update_Index(TestCase):
    def add_index(self):
        """新增一个索引，并返回新增后的索引数量"""
        # 先获取初始已有索引数量
        _bool = self.element_is_exist("tbody:nth-child(1) > tr")
        index_sum = 0
        if _bool:
            index_sum = len(self.get_elements("tbody:nth-child(1) > tr"))

        # 新增一个索引
        self.click("#addBtn")
        self.click("#updateTimeMin")
        self.click("#laydate_ok")
        self.click("#updateTimeMax")
        self.click("#laydate_ok")
        self.select("#updateIndex", "2")
        self.sleep(1)
        self.click(".ui-dialog-buttonset .ui-button-text")

        return index_sum + 1

    def del_index(self, index_sum):
        """删除新增的索引"""
        self.click(f"tbody:nth-child(1) > tr:nth-child({index_sum}) > td:nth-child(1)")
        self.click("#deleteBtn")
        self.click("xpath=>//div[5]/div[3]/div/button/span")
        self.click(".ui-button-text:nth-child(1)")

    @classmethod
    def setUpClass(cls):
        cls.driver = Pyse("chrome")
        platform_api.login_platform(cls.driver)

    def test_open_update_index(self):
        """[系统管理]--[更新索引]，验证更新索引页面回显信息"""
        platform_api.open_page(self, 1, "更新索引")

        # 此页面是嵌套在一个frame里的，所以这儿要切换一下
        self.switch_to_frame(0)

        # 验证[运行]按钮是否存在
        self.assertTrue(self.element_is_exist("#runBtn"))

        # 验证[新增]按钮是否存在
        self.assertTrue(self.element_is_exist("#addBtn"))

        # 验证[修改]按钮是否存在
        self.assertTrue(self.element_is_exist("#updateBtn"))

        # 验证[删除]按钮是否存在
        self.assertTrue(self.element_is_exist("#deleteBtn"))

    def test_add_index(self):
        """[系统管理]--[更新索引]，新增一个索引"""
        platform_api.open_page(self, 1, "更新索引")

        # 切换frame
        self.switch_to_frame(0)

        # 新增一个索引
        index_sum = self.add_index()

        # 验证新增索引是否成功
        self.sleep(2)
        bool_ = self.element_is_exist("tbody:nth-child(1) > tr")
        self.assertTrue(bool_)
        if bool_:
            self.assertEqual(index_sum, len(self.get_elements("tbody:nth-child(1) > tr")))

        # 清除测试数据
        self.del_index(index_sum)

    def test_update_index(self):
        """[系统管理]--[更新索引]，修改一个索引"""
        platform_api.open_page(self, 1, "更新索引")

        # 切换frame
        self.switch_to_frame(0)

        # 先新增一个索引
        index_sum = self.add_index()

        # 修改索引
        self.sleep(1)
        self.click(f"tbody:nth-child(1) > tr:nth-child({index_sum}) > td:nth-child(1)")
        self.click("#updateBtn")
        self.select("#updateIndex", "1")
        self.sleep(1)
        self.click("xpath=>//div[4]/div[3]/div/button/span")

        # 验证索引是否修改成功
        self.sleep(2)
        text = self.get_text(f"tbody:nth-child(1) > tr:nth-child({index_sum}) > td:nth-child(4)")
        self.assertEqual("录音索引", text)

        # 清除测试数据
        self.del_index(index_sum)

    def test_run_index(self):
        """[系统管理]--[更新索引]，运行一个索引"""
        platform_api.open_page(self, 1, "更新索引")

        # 切换frame
        self.switch_to_frame(0)

        # 先新增一个索引
        index_sum = self.add_index()

        # 运行索引
        self.sleep(1)
        self.click(f"tbody:nth-child(1) > tr:nth-child({index_sum}) > td:nth-child(1)")
        self.click("#runBtn")

        # 验证运行索引是否成功
        self.sleep(1)
        text = self.get_text("#message-basic-modal-content1 > div")
        self.assertEqual("更新成功", text)
        self.click("xpath=>//div[3]/div/button/span")

        # 清除测试数据
        self.del_index(index_sum)

    def test_del_index(self):
        """[系统管理]--[更新索引]，删除一个索引"""
        platform_api.open_page(self, 1, "更新索引")

        # 切换frame
        self.switch_to_frame(0)

        # 先新增一个索引
        index_sum = self.add_index()

        # 删除新增的索引
        self.sleep(1)
        self.click(f"tbody:nth-child(1) > tr:nth-child({index_sum}) > td:nth-child(1)")
        self.click("#deleteBtn")
        self.click("xpath=>//div[5]/div[3]/div/button/span")

        # 验证索引是否删除成功
        text = self.get_text("#message-basic-modal-content1 > div")
        self.assertEqual("删除成功", text)

        self.click(".ui-button-text:nth-child(1)")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    TestRunner().debug()
