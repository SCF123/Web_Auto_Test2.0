import unittest
from .selenium_api import WebDriver
from selenium_lib.weblog import MyLog
from time import sleep

logger = MyLog().get_logger()
class TestCase(unittest.TestCase, WebDriver):
    def assertTitle(self, title, second=3):
        """
        断言当前页面标题是否符合预期。

        Usage:
        self.assertTitle("title")
        """
        if title is None:
            logger.error("'title' 不能为空！")
        for s in range(second):
            try:
                self.assertIn(title, self.get_title())
                break
            except AssertionError:
                sleep(1)
        else:
            self.assertIn(title, self.get_title())

    def assertUrl(self, url, second=3):
        """
        断言当前页面URL是否符合预期。

        Usage:
        self.assertUrl("url")
        """
        if url == None:
            logger.error("'URL' 不能为空！")
        for s in range(second):
            try:
                self.assertEqual(url, self.get_url())
            except AssertionError:
                sleep(1)
        else:
            self.assertEqual(url, self.get_url())

    def assertText(self, actual_el, expect_result):
        """
        断言当前页面某个标签的文本是否符合预期。
        - actual_el: 实际文本的定位元素
        - expect_result :预期的文本

        Usage:
        self.assertText("#el","text")
        """
        if actual_el is None or expect_result is None:
            logger.error("'actual(实际的文本定位元素)' 或 'exect(预期的文本)' 不能为空！")
        actual_result = self.get_text(actual_el)
        self.assertEqual(actual_result, expect_result)

    def assertAlert(self, expect_text):
        """
        断言弹窗的警告文本是否符合预期
        - expect_text :预期的文本

        Usage:
        self.assertText("text")
        """
        if expect_text is None:
            logger.error("预期的文本内容不能为空！")
        alert_text = self.get_alert_text()
        self.assertEqual(alert_text, expect_text)
