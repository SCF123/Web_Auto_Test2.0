from BeautifulReport import BeautifulReport  # 引入BeautifulReport模块
from selenium_lib import Pyse, TestCase, TestRunner
import time, unittest


class TestBaidu(TestCase):
    def setUp(self):
        self.driver = Pyse("chrome")
        self.wait(10)
        self.open("https://www.baidu.com")
        self.sleep(2)

    # 打开百度, 点击新闻按钮前截一次图，在点击新闻按钮后再截一次图
    # 这里add_test_img参数即相应的截图名称，必须要与save_img参数一致
    @BeautifulReport.add_test_img('点击新闻按钮前', '点击新闻按钮后')
    def test_news(self):
        """新闻按钮跳转"""
        # self.get_screenshot('点击新闻按钮前')
        self.click('link_text=>新闻')
        # self.get_screenshot('点击新闻按钮后')
        self.assertTitle('百度新闻')

    # 如果在测试过程中, 出现不确定的错误, 程序会自动截图, 并返回失败。
    # 此时add_test_img参数必须是用例方法名，这个名字也将是截图名
    # @BeautifulReport.add_test_img('test_map')
    def test_map(self):
        """地图按钮跳转"""
        # 此处故意设置使定位失败
        self.click('link_text=>地图的')
        # 此处故意使校验失败
        self.assertTitle('百度地图')

    # 如果用例没有出现错误, 即使用了错误截图装饰器, 也不会影响用例的使用，也不会截图
    @unittest.skip("I don't want to run the case")  # 跳过此用例不执行
    # @BeautifulReport.add_test_img('test_academic')
    def test_academic(self):
        """学术按钮跳转"""
        print(self.get_attribute_by_js("#kw", "maxlength"))
        self.click('link_text=>学术')
        self.assertTitle('百度学术')

    def tearDown(self):
        time.sleep(3)
        self.driver.quit()


# 此部分用于调试单个用例文件，在执行所有用例文件时并不会有所影响
if __name__ == "__main__":
    runner = TestRunner('QA', '百度测试用例', '测试环境：Chrome')
    # runner.run()
    runner.debug()


'''
说明：
'QA' ： 设置执行此用例的人员名称， 默认是QA；
'百度测试用例' ： 指定测试报告中项目的标题；
'测试环境：Chrome' ： 指定测试环境描述。

debug() # debug模式可用于调试单个测试用例文件，但需要注释掉截图的接口，执行用例时不会生成测试报告；
run()   # run模式执行用例会生成测试报告。
'''


