#!/usr/bin/python

from .test_runner import TestRunner
from .selenium_api import WebDriver
from .selenium_case import TestCase
from .browser_driver import Pyse
from .common import Readconfig, send_mail, skip_testcase
from .weblog import MyLog

__author__ = "非攻scf"

__version__ = "2.0"


"""
2.0 version update:
主要将selenium的原生接口进行二次封装，使用例编写更简单

多级定位有待完善
用例执行方式有待商榷
用例跳过不执行机制有待补充
"""