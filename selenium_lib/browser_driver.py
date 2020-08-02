from selenium_lib.weblog import MyLog
from selenium import webdriver

logger = MyLog().get_logger()


def Pyse(browser):
    """
    只支持常用的四种浏览器：
        谷歌浏览器参数是：chrome
        火狐浏览器参数是：firefox
        IE浏览器参数是：ie
        Edge浏览器参数是：edge
    """
    if browser == "firefox":
        return webdriver.Firefox()
    elif browser == "chrome":
        return webdriver.Chrome()
    elif browser == "ie":
        return webdriver.Ie()
    elif browser == 'edge':
        return webdriver.Edge()
    else:
        logger.error("Not found %s browser,You can enter 'chrome', 'firefox', 'ie', 'edge'." % browser, exc_info=True)
