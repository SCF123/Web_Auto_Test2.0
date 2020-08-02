"""
用例作者：scf
用例明细：
    test_open_standard_code(self):[标准代码]--验证标准代码页面回显信息
    test_add_classify(self):[标准代码]--新增一个分类
    test_update_classify(self):[标准代码]--修改一个分类
    test_del_classify(self):[标准代码]--删除一个分类
    test_query_standard_code(self):[标准代码]--查询一个代码
    test_add_standard_code(self):[标准代码]--新增一个标准代码
    test_update_standard_code(self):[标准代码]--修改一个标准代码
    test_del_standard_code(self):[标准代码]--修改一个标准代码

"""

from selenium_lib import Pyse, TestCase, TestRunner
from testcase.common import platform_api


class Test_Standard_Code(TestCase):
    def add_classify(self, classify_name, classify_code):
        """新增一个分类"""
        self.click(".item1 span")
        self.clear("xpath=>//input[@type='text']")
        self.type("xpath=>//input[@type='text']", classify_name)
        self.clear("xpath=>(//input[@type='text'])[2]")
        self.type("xpath=>(//input[@type='text'])[2]", classify_code)
        self.click("#menu > div:nth-child(3) .ivu-btn-primary")

    def del_classify(self, classify_name):
        """删除一个分类"""
        self.click(f"xpath=>//span[contains(.,'{classify_name}')]")
        self.click(".cur .delete-btn > .icon")
        self.sleep(1)
        self.click("div:nth-child(5) .ivu-btn-large:nth-child(1) > span")
        self.sleep(1)

    def add_standard_code(self, code_name, code):
        """新增一个标准代码"""
        self.click(".ut-toolbar:nth-child(2) > .ivu-btn > span")
        self.clear("xpath=>(//input[@type='text'])[6]")
        self.type("xpath=>(//input[@type='text'])[6]", code_name)
        self.clear("xpath=>(//input[@type='text'])[7]")
        self.type("xpath=>(//input[@type='text'])[7]", code)
        self.click("div:nth-child(2) > .ivu-modal-wrap .ivu-btn-large:nth-child(1) > span")

    def del_standard_code(self, code_name):
        """删除一个标准代码"""
        self.clear("#searchTitle > .ivu-input")
        self.type("#searchTitle > .ivu-input", code_name)
        self.click(".ivu-icon-search")
        self.sleep(1)
        self.click("xpath=>//tr/td[4]/div/div/a[2]")
        self.click(".ut-grid-middle .ivu-btn:nth-child(1) > span")
        self.sleep(1)

    def add_kv(self, kv_name, kv_code):
        """新增一个键值"""
        self.click(".ut-btn-mgr10 > span")
        self.clear("xpath=>(//input[@type='text'])[13]")
        self.type("xpath=>(//input[@type='text'])[13]", kv_code)
        self.clear("xpath=>(//input[@type='text'])[14]")
        self.type("xpath=>(//input[@type='text'])[14]", kv_name)
        self.click(".ut-grid-top > div:nth-child(2) > .ivu-modal-wrap .ivu-btn:nth-child(1) > span")

    @classmethod
    def setUpClass(cls):
        cls.driver = Pyse("chrome")
        cls.driver.maximize_window()
        platform_api.login_platform(cls.driver)

    def test_open_standard_code(self):
        """[标准代码]--验证标准代码页面回显信息"""
        platform_api.open_page(self, 1, "标准代码")

        # 验证[新增分类]按钮是否存在
        self.assertTrue(self.element_is_exist(".item1 span"))

        # 验证[新增代码]按钮是否存在
        self.assertTrue(self.element_is_exist(".ut-toolbar:nth-child(2) > .ivu-btn > span"))

        # 验证[搜索输入框]是否存在
        self.assertTrue(self.element_is_exist("#searchTitle > .ivu-input"))

        # 验证[搜索]按钮是否存在
        self.assertTrue(self.element_is_exist(".ivu-icon-search"))

        # 验证[新增键值]按钮是否存在
        self.assertTrue(self.element_is_exist(".ut-btn-mgr10 > span"))

        # 验证[上移]按钮是否存在
        self.assertTrue(self.element_is_exist(".ml6:nth-child(2) > span"))

        # 验证[下移]按钮是否存在
        self.assertTrue(self.element_is_exist(".ml6:nth-child(3) > span"))

    def test_add_classify(self):
        """[标准代码]--新增一个分类"""
        platform_api.open_page(self, 1, "标准代码")

        # 新增一个分类
        self.add_classify("测试新增分类", "110001")

        # 验证新增分类是否成功
        self.sleep(2)
        elements = self.get_elements("xpath=>//div[@id='sites']/div")
        text = []
        for i in range(1, len(elements)+1):
            text.append(self.get_text(f"xpath=>//div[@id='sites']/div[{i}]/div/span"))

        self.assertIn("测试新增分类", text)

        # 清除测试数据
        self.sleep(2)
        self.del_classify("测试新增分类")

    def test_update_classify(self):
        """[标准代码]--修改一个分类"""
        platform_api.open_page(self, 1, "标准代码")

        # 先新增一个分类
        self.add_classify("测试修改分类", "110002")

        # 修改分类
        self.sleep(2)
        self.click("xpath=>//span[contains(.,'测试修改分类')]")
        self.click(".cur .write-btn > .icon")
        self.clear("xpath=>(//input[@type='text'])[3]")
        self.type("xpath=>(//input[@type='text'])[3]", "测试分类改")
        self.click("#menu > div:nth-child(4) .ivu-btn-primary > span")

        # 验证修改分类是否成功
        self.sleep(2)
        elements = self.get_elements("xpath=>//div[@id='sites']/div")
        text = []
        for i in range(1, len(elements) + 1):
            text.append(self.get_text(f"xpath=>//div[@id='sites']/div[{i}]/div/span"))

        self.assertIn("测试分类改", text)

        # 清除测试数据
        self.sleep(2)
        self.del_classify("测试分类改")

    def test_del_classify(self):
        """[标准代码]--删除一个分类"""
        platform_api.open_page(self, 1, "标准代码")

        # 先新增一个分类
        self.add_classify("测试删除分类", "110003")

        # 再删除
        self.sleep(2)
        self.del_classify("测试删除分类")

        # 验证删除分类是否成功
        self.sleep(1)
        elements = self.get_elements("xpath=>//div[@id='sites']/div")
        text = []
        for i in range(1, len(elements) + 1):
            text.append(self.get_text(f"xpath=>//div[@id='sites']/div[{i}]/div/span"))

        self.assertNotIn("测试删除分类", text)

    def test_query_standard_code(self):
        """[标准代码]--查询一个代码"""
        platform_api.open_page(self, 1, "标准代码")

        # 查询[报表基础数据]中的[参数类型]
        self.clear("#searchTitle > .ivu-input")
        self.type("#searchTitle > .ivu-input", "参数类型")
        self.sleep(1)
        self.click(".ivu-icon-search")

        # 验证代码查询是否成功
        self.sleep(1)
        code_name = self.get_text("xpath=>//tr[@id='tr_Root_undefined']/td[2]/div/span")
        self.assertEqual("参数类型", code_name)

    def test_add_standard_code(self):
        """[标准代码]--新增一个标准代码"""
        platform_api.open_page(self, 1, "标准代码")

        # 先新增一个分类
        self.add_classify("测试新增代码", "110004")

        # 再新增代码
        self.sleep(2)
        self.click("xpath=>//span[contains(.,'测试新增代码')]")
        self.add_standard_code("测试代码", "test001")

        # 验证代码是否新增成功
        self.sleep(1)
        text = []
        num = len(self.get_elements("#tr_Root_undefined"))
        for i in range(1, num + 1):
            code_name = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/span)[{i}]")
            text.append(code_name)

        self.assertIn("测试代码", text)

        # 清除测试数据
        self.sleep(1)
        self.del_standard_code("测试代码")
        self.del_classify("测试新增代码")

    def test_update_standard_code(self):
        """[标准代码]--修改一个标准代码"""
        platform_api.open_page(self, 1, "标准代码")

        # 先新增一个分类
        self.add_classify("测试修改代码", "110005")
        # 新增一个代码
        self.sleep(2)
        self.click("xpath=>//span[contains(.,'测试修改代码')]")
        self.add_standard_code("代码修改", "test002")

        # 修改新增的代码
        self.sleep(1)
        self.clear("#searchTitle > .ivu-input")
        self.type("#searchTitle > .ivu-input", "代码修改")
        self.sleep(1)
        self.click(".ivu-icon-search")
        self.sleep(1)
        self.click("xpath=>//tr/td[4]/div/div/a")
        self.sleep(1)
        self.clear("xpath=>(//input[@type='text'])[10]")
        self.type("xpath=>(//input[@type='text'])[10]", "修改代码")
        self.clear("xpath=>(//input[@type='text'])[11]")
        self.type("xpath=>(//input[@type='text'])[11]", "test_02")
        self.sleep(1)
        self.click("div:nth-child(4) .ivu-btn-large:nth-child(1) > span")

        # 验证代码是否修改成功
        self.sleep(2)
        text = []
        num = len(self.get_elements("#tr_Root_undefined"))
        for i in range(1, num + 1):
            code_name = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/span)[{i}]")
            text.append(code_name)

        self.assertIn("修改代码", text)

        # 清除测试数据
        self.sleep(1)
        self.del_standard_code("修改代码")
        self.del_classify("测试修改代码")

    def test_del_standard_code(self):
        """[标准代码]--删除一个标准代码"""
        platform_api.open_page(self, 1, "标准代码")

        # 先新增一个分类
        self.add_classify("测试删除代码", "110006")
        # 新增一个代码
        self.sleep(2)
        self.click("xpath=>//span[contains(.,'测试删除代码')]")
        self.add_standard_code("删除代码", "test002")

        # 删除新增的代码
        self.sleep(1)
        self.del_standard_code("删除代码")

        # 验证代码是否删除成功
        text = self.get_text(".ivu-message .ivu-message-success >span")
        self.assertEqual(text, "删除成功！")

        # 清除测试数据
        self.sleep(2)
        self.del_classify("测试删除代码")

    def test_add_kv(self):
        """[标准代码]--新增一个键值"""
        platform_api.open_page(self, 1, "标准代码")

        # 先新增一个分类
        self.add_classify("测试新增键值", "110007")
        # 新增一个代码
        self.sleep(2)
        self.click("xpath=>//span[contains(.,'测试新增键值')]")
        self.add_standard_code("测试代码1", "kv_001")

        # 新增一个键值
        self.sleep(2)
        self.add_kv("测试键值", "test_kv1")

        # 验证新增键值是否成功
        self.sleep(2)
        text = []
        num = len(self.get_elements("#tr_Root_undefined"))
        for i in range(1, num + 1):
            code_name = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/span)[{i}]")
            text.append(code_name)
        self.assertIn("测试键值", text)

        # 清除测试数据
        self.sleep(2)
        self.del_standard_code("测试代码1")
        self.del_classify("测试新增键值")

    def test_del_kv(self):
        """[标准代码]--删除一个键值"""
        platform_api.open_page(self, 1, "标准代码")

        # 先新增一个分类
        self.add_classify("测试删除键值", "110008")
        # 新增一个代码
        self.sleep(2)
        self.click("xpath=>//span[contains(.,'测试删除键值')]")
        self.add_standard_code("测试代码2", "kv_002")
        # 新增一个键值
        self.sleep(2)
        self.add_kv("删除键值", "del_kv1")

        # 删除新增的键值
        self.sleep(2)
        self.click("xpath=>//tr/td[3]/div/div/a")
        self.click(".ut-grid-top > div:nth-child(3) .ivu-btn:nth-child(1) > span")

        # 验证键值是否删除成功
        self.sleep(2)
        text = []
        num = len(self.get_elements("#tr_Root_undefined"))
        for i in range(1, num + 1):
            code_name = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/span)[{i}]")
            text.append(code_name)

        self.assertNotIn("删除键值", text)

        # 清除测试数据
        self.sleep(1)
        self.del_standard_code("测试代码2")
        self.del_classify("测试删除键值")

    def test_up_kv(self):
        """[标准代码]--上移键值"""
        platform_api.open_page(self, 1, "标准代码")

        # 先新增一个分类
        self.add_classify("测试上移键值", "110009")
        # 新增一个代码
        self.sleep(2)
        self.click("xpath=>//span[contains(.,'测试上移键值')]")
        self.add_standard_code("测试代码3", "kv_003")
        # 新增两个键值
        self.sleep(2)
        self.add_kv("上移键值1", "up_kv1")
        self.sleep(2)
        self.add_kv("上移键值2", "up_kv2")

        # 上移键值2
        self.sleep(2)
        num = len(self.get_elements("#tr_Root_undefined"))
        for i in range(1, num + 1):
            code_name = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/span)[{i}]")
            if "上移键值2" == code_name:
                self.click(f"xpath=>(//tr[@id='tr_Root_undefined'])[{i}]")
                self.click(".ml6:nth-child(2) > span")
                break

        # 验证上移键值是否成功
        text = self.get_text(".ivu-message .ivu-message-success >span")
        self.assertEqual(text, "移动成功")

        # 清除测试数据
        self.sleep(1)
        self.del_standard_code("测试代码3")
        self.del_classify("测试上移键值")

    def test_down_kv(self):
        """[标准代码]--下移键值"""
        platform_api.open_page(self, 1, "标准代码")

        # 先新增一个分类
        self.add_classify("测试下移键值", "110010")
        # 新增一个代码
        self.sleep(2)
        self.click("xpath=>//span[contains(.,'测试下移键值')]")
        self.add_standard_code("测试代码4", "kv_004")
        # 新增两个键值
        self.sleep(2)
        self.add_kv("下移键值1", "down_kv1")
        self.sleep(2)
        self.add_kv("下移键值2", "down_kv2")

        # 下移键值1
        self.sleep(2)
        num = len(self.get_elements("#tr_Root_undefined"))
        for i in range(1, num + 1):
            code_name = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/span)[{i}]")
            if "下移键值1" == code_name:
                self.click(f"xpath=>(//tr[@id='tr_Root_undefined'])[{i}]")
                self.click(".ml6:nth-child(3) > span")
                break

        # 验证上移键值是否成功
        text = self.get_text(".ivu-message .ivu-message-success >span")
        self.assertEqual(text, "移动成功")

        # 清除测试数据
        self.sleep(1)
        self.del_standard_code("测试代码4")
        self.del_classify("测试下移键值")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    TestRunner().debug()
