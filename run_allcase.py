from selenium_lib import TestRunner

if __name__ == "__main__":
    runner = TestRunner("scf", "技术开发平台回归测试用例执行", "测试环境： Chrome")
    runner.run()

"""
此文件是总的用例执行文件，会在result/testreport目录下生成HTML形式的测试报告。
执行此文件前，请先查看配置文件web_auto.ini中的配置是否都正确
"""
