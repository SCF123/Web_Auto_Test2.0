from selenium_lib.common import *
from BeautifulReport import BeautifulReport
import unittest, time, os
from multiprocessing.dummy import Pool


class TestRunner(object):
    def __init__(self, testor="QA",title="UI自动化测试报告",description="测试用例批量执行"):
        self.testor = testor
        self.title = title
        self.des = description
        # 获取当前时间，并转化成我们想要的格式
        self.now_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))
        # 拼接测试报告名，固定名TestReport + 当前时间
        self.report_name = 'TestReport_' + self.now_time + '.html'
        # 拼接测试报告存放路径
        self.report_path = os.path.join(
            os.path.split(os.path.realpath(__file__))[0][:-12],
            'result\\testreport'
        )

    # 使用discover方法加载所有test_开头的测试用例
    def add_suite(self):
        case_file = os.path.join(os.getcwd(), 'testcase')
        discover = unittest.defaultTestLoader.discover(
            case_file,
            pattern='test_*.py',
            top_level_dir=None
        )
        return discover


    # 调用BeautifulReport模块执行测试用例并生成测试报告
    def run_case(self, suites):
        result = BeautifulReport(suites)
        result.report(filename=self.report_name,
                      tester=self.testor,
                      title=self.title,
                      description=self.des,
                      log_path=self.report_path
                      )

    # 使用多线程去并行执行测试用例，开了4个线程
    def start_thread(self, suites):
        pool = Pool(4)
        pool.map(self.run_case, suites)
        pool.close()
        pool.join()

    # 执行debug跑用例不会生成测试报告，用于调试单个用例代码
    def debug(self):
        test_suites = self.add_suite()
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(test_suites)


    # 执行用例，生成测试报告
    def run(self):
        skip_testcase()
        test_suites = self.add_suite()
        self.start_thread(test_suites)

        switch = Readconfig().get_value("Email", "switch")
        if int(switch) == 1:
            # 所有用例执行完成后，将生成的测试报告通过邮件发送
            filename = '{}\\{}'.format(self.report_path, self.report_name)
            text = "最新Web自动化测试报告请接收，见附件。"
            send_mail(text, filename)

