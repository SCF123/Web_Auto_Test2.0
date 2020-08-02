from selenium_lib.weblog import MyLog
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select
import time, os


logger = MyLog().get_logger()
class WebDriver(object):
    """
       对selenium原生接口进行二次封装，使之更易使用
    """

    original_window = None

    def wait_element(self, el):
        """
        等待元素显示出来
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(el)
            )
        except TimeoutException:
            return False
        else:
            return True

    def get_element(self, css):
        """
        判断元素定位方式，并返回元素。
        """
        if "=>" not in css:
            by = "css"
            value = css
        else:
            by = css.split("=>")[0]
            value = css.split("=>")[1]
            if by == "" or value == "":
                logger.error("元素定位使用语法错误，参考语法：'id=>useranme'。")

        time_out_error = "定位元素超时，请尝试其他定位方式！"
        if by == "id":
            req = self.wait_element((By.ID, value))
            if req is True:
                element = self.driver.find_element_by_id(value)
            else:
                logger.error("[{}=>{}], {}".format(by, value, time_out_error), exc_info=True)
        elif by == "name":
            req = self.wait_element((By.NAME, value))
            if req is True:
                element = self.driver.find_element_by_name(value)
            else:
                logger.error("{}=>{}, {}".format(by, value, time_out_error), exc_info=True)
        elif by == "class":
            req = self.wait_element((By.CLASS_NAME, value))
            if req is True:
                element = self.driver.find_element_by_class_name(value)
            else:
                logger.error("{}=>{}, {}".format(by, value, time_out_error), exc_info=True)
        elif by == "link_text":
            req = self.wait_element((By.LINK_TEXT, value))
            if req is True:
                element = self.driver.find_element_by_link_text(value)
            else:
                logger.error("{}=>{}, {}".format(by, value, time_out_error), exc_info=True)
        elif by == "xpath":
            req = self.wait_element((By.XPATH, value))
            if req is True:
                element = self.driver.find_element_by_xpath(value)
            else:
                logger.error("{}=>{}, {}".format(by, value, time_out_error), exc_info=True)
        elif by == "css":
            req = self.wait_element((By.CSS_SELECTOR, value))
            if req is True:
                element = self.driver.find_element_by_css_selector(value)
            else:
                logger.error("{}=>{}, {}".format(by, value, time_out_error), exc_info=True)
        else:
            logger.error("请输入正确的目标元素属性，如：'id','name','class','link_text','xpath','css'。")
        return element

    def get_elements(self, css):
        """
        判断元素定位方式，并返回以该定位方式定位到的所有标签。
        """
        if "=>" not in css:
            by = "css"
            value = css
        else:
            by = css.split("=>")[0]
            value = css.split("=>")[1]
            if by == "" or value == "":
                logger.error("元素定位使用语法错误，参考语法：'id=>useranme'。")

        time_out_error = "定位元素超时，请尝试其他定位方式！"
        if by == "id":
            req = self.wait_element((By.ID, value))
            if req is True:
                elements = self.driver.find_elements_by_id(value)
            else:
                logger.error("[{}=>{}], {}".format(by, value, time_out_error), exc_info=True)
        elif by == "name":
            req = self.wait_element((By.NAME, value))
            if req is True:
                elements = self.driver.find_elements_by_name(value)
            else:
                logger.error("{}=>{}, {}".format(by, value, time_out_error), exc_info=True)
        elif by == "class":
            req = self.wait_element((By.CLASS_NAME, value))
            if req is True:
                elements = self.driver.find_elements_by_class_name(value)
            else:
                logger.error("{}=>{}, {}".format(by, value, time_out_error), exc_info=True)
        elif by == "link_text":
            req = self.wait_element((By.LINK_TEXT, value))
            if req is True:
                elements = self.driver.find_elements_by_link_text(value)
            else:
                logger.error("{}=>{}, {}".format(by, value, time_out_error), exc_info=True)
        elif by == "xpath":
            req = self.wait_element((By.XPATH, value))
            if req is True:
                elements = self.driver.find_elements_by_xpath(value)
            else:
                logger.error("{}=>{}, {}".format(by, value, time_out_error), exc_info=True)
        elif by == "css":
            req = self.wait_element((By.CSS_SELECTOR, value))
            if req is True:
                elements = self.driver.find_elements_by_css_selector(value)
            else:
                logger.error("{}=>{}, {}".format(by, value, time_out_error), exc_info=True)
        else:
            logger.error("请输入正确的目标元素属性，如：'id','name','class','link_text','xpath','css'。")
        return elements

    def open(self, url):
        """
        打开网址

        Usage:
        driver.open("https://www.baidu.com")
        """
        self.driver.get(url)

    def max_window(self):
        """
        设置浏览器窗口最大化

        Usage:
        driver.max_window()
        """
        self.driver.maximize_window()

    def set_window(self, width, hight):
        """
        自定义设置浏览器窗口大小

        Usage:
        driver.set_window(width,hight)
        """
        self.driver.set_window_size(width, hight)

    def type(self, css, text):
        """
        操作输入框：定位输入框并向其中输入内容

        Usage:
        driver.type("css=>#el","selenium")
        """
        el = self.get_element(css)
        el.send_keys(text)

    def clear(self, css):
        """
        清空输入框中的内容

        Usage:
        driver.clear("css=>#el")
        """
        el = self.get_element(css)
        el.clear()

    def click(self, css):
        """
        定位标签并点击

        Usage:
        driver.click("css=>#el")
        """
        el = self.get_element(css)
        el.click()

    def right_click(self, css):
        """
        模拟鼠标右击标签

        Usage:
        driver.right_click("css=>#el")
        """
        el = self.get_element(css)
        ActionChains(self.driver).context_click(el).perform()

    def move_to_element(self, css):
        """
        模拟鼠标悬停在标签上

        Usage:
        driver.move_to_element("css=>#el")
        """
        el = self.get_element(css)
        ActionChains(self.driver).move_to_element(el).perform()

    def double_click(self, css):
        """
        模拟鼠标双击标签

        Usage:
        driver.double_click("css=>#el")
        """
        el = self.get_element(css)
        ActionChains(self.driver).double_click(el).perform()

    def drag_and_drop(self, el_css, ta_css):
        """
        在源标签上按下鼠标左键，然后拖动到目标标签上释放

        Usage:
        driver.drag_and_drop("css=>#el","css=>#ta")
        """
        element = self.get_element(el_css)
        target = self.get_element(ta_css)
        ActionChains(self.driver).drag_and_drop(element, target).perform()

    def drag_and_drop_by_offset(self, css, x, y):
        """
        在源标签上按下鼠标左键，然后拖动到目标坐标（x，y）上释放

        Usage:
        driver.drag_and_drop_by_offset("css=>#el", 100, 500)
        """
        el = self.get_element(css)
        ActionChains(self.driver).drag_and_drop_by_offset(el, xoffset=x, yoffset=y).perform()

    def click_text(self, text):
        """
        点击标签的链接文本

        Usage:
        driver.click_text("新闻")
        """
        self.driver.find_element_by_partial_link_text(text).click()

    def close(self):
        """
        关闭浏览器中的一个窗口或标签

        Usage:
        driver.close()
        """
        self.driver.close()

    def quit(self):
        """
        退出浏览器驱动程序，并关闭所有窗口。即关闭浏览器。

        Usage:
        driver.quit()
        """
        self.driver.quit()

    def submit(self, css):
        """
        提交指定的表单

        Usage:
        driver.submit("css=>#el")
        """
        el = self.get_element(css)
        el.submit()

    def F5(self):
        """
        模拟F5键，刷新页面

        Usage:
        driver.F5()
        """
        self.driver.refresh()

    def get_attribute(self, css, attribute):
        """
        获取标签属性值

        Usage:
        driver.get_attribute("css=>#el","type")
        """
        el = self.get_element(css)
        return el.get_attribute(attribute)

    def get_text(self, css):
        """
        获取标签的文本内容

        Usage:
        driver.get_text("css=>#el")
        """
        el = self.get_element(css)
        return el.text

    def get_display(self, css):
        """
        判断标签是否用户可见，是返回True，否返回False

        Usage:
        driver.get_display("css=>#el")
        """
        el = self.get_element(css)
        return el.is_displayed()

    def get_title(self):
        """
        获取浏览器窗口的title

        Usage:
        driver.get_title()
        """
        return self.driver.title

    def get_url(self):
        """
        获取当前页面的URL地址

        Usage:
        driver.get_url()
        """
        return self.driver.current_url

    def get_alert_text(self):
        """
        获取Alert弹窗内的文本内容

        Usage:
        driver.get_alert_text()
        """
        return self.driver.switch_to.alert.text

    def wait(self, secs):
        """
        设置全局隐式等待

        Usage:
        driver.wait(10)
        """
        self.driver.implicitly_wait(secs)

    def accept_alert(self):
        """
        确认警告框，相当于点击Alert警告窗上的确定按钮

        Usage:
        driver.accept_alert()
        """
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self):
        """
        拒绝可用的警告，相当于点击Alert警告窗上的取消按钮

        Usage:
        driver.dismiss_alert()
        """
        self.driver.switch_to.alert.dismiss()

    def switch_to_frame(self, css):
        """
        切换到指定的frame

        Usage:
        driver.switch_to_frame(0)
        driver.switch_to_frame("css=>#el")
        """
        if type(css) is int:
            self.driver.switch_to.frame(css)
        else:
            iframe_el = self.get_element(css)
            self.driver.switch_to.frame(iframe_el)

    def switch_to_frame_out(self):
        """
        将当前 frame 切换到默认的 frame，一般是页面主体 frame

        Usage:
        driver.switch_to_frame_out()
        """
        self.driver.switch_to.default_content()

    def switch_to_parent_frame(self):
        """
        将当前 frame 切换到上一级（父级）的 frame

        Usage:
        driver.switch_to_frame_out()
        """
        self.driver.switch_to.parent_frame()

    def open_new_window(self, css):
        """
        打开新的窗口并将句柄切换到新打开的窗口。

        Usage:
        driver.open_new_window("link_text=>注册")
        """
        original_window = self.driver.current_window_handle
        el = self.get_element(css)
        el.click()
        all_handles = self.driver.window_handles
        for handle in all_handles:
            if handle != original_window:
                self.driver.switch_to.window(handle)

    def get_screenshot(self, img_name):
        """
        将当前窗口的屏幕快照以PNG图像文件形式保存到./Auto_UITest/result/img路径下。

        Usage:
        driver.get_screenshot('img_name')
        """
        self.driver.get_screenshot_as_file(
            '{}/{}.png'.format(
                os.path.abspath('result\\img'),
                img_name)
        )

    def select(self, sele_css, op_value):
        """
        定位select标签，并选择一个option（选项）
        :Args:
         - css - element SELECT element to wrap
         - value - The value to match against

        Usage:
            <select name="NR" id="nr">
                <option value="10" selected="">每页显示10条</option>
                <option value="20">每页显示20条</option>
                <option value="50">每页显示50条</option>
            </select>

            driver.select("#nr", '20')
            driver.select("xpath=>//[@name='NR']", '20')
        """
        el = self.get_element(sele_css)
        Select(el).select_by_value(op_value)

    def sleep(self, sec):
        """
        延迟
        """
        time.sleep(sec)

    def run_js(self, script):
        """
        执行JavaScript脚本。

        Usage:
        driver.run_js("window_scroll(0, 500)")
        """
        return self.driver.execute_script(script)

    def display_by_js(self, css_selector):
        """
        JavaScript API, 只支持CSS方式定位
        使隐藏的元素显示

        Usage:
        driver.display_by_js("#css")
        """
        js = """var elm = document.querySelector("{css}");
                    elm.style.display = "block";""".format(css=css_selector)
        self.run_js(js)

    def remove_attribute_by_js(self, css_selector, attribute):
        """
        JavaScript API, 只支持CSS方式定位
        删除标签元素的属性

        Usage:
        driver.remove_attribute_by_js("#css_selector", "attribute")
        """
        js = """var elm = document.querySelector("{css}");
                    elm.removeAttribute("{attr}");""".format(css=css_selector, attr=attribute)
        self.run_js(js)

    def get_attribute_by_js(self, css_selector, attribute):
        """
        JavaScript API, 只支持CSS方式定位
        通过执行JS语句的方法，获取标签元素属性

        Usage:
        driver.get_attribute_by_js("#css_selector", "attribute")
        """
        js = """return document.querySelector("{css}").getAttribute("{attr}");""".format(
            css=css_selector, attr=attribute)
        return self.run_js(js)

    def set_attribute_by_js(self, css_selector, attribute, value):
        """
        JavaScript API, 只支持CSS方式定位
        给标签元素设置一个属性

        Usage:
        driver.set_attribute_by_js("#css_selector", "attribute", "value")
        """
        js = """var elm = document.querySelector("{css}");
                    elm.setAttribute("{attr}", "{value}");
                    """.format(css=css_selector, attr=attribute, value=value)
        self.run_js(js)

    def clear_style_by_js(self, css_selector):
        """
        JavaScript API, 只支持CSS方式定位
        清除标签的样式

        Usage:
        driver.clear_style_by_js("#css")
        """
        js = """var elm = document.querySelector("{css}");
                    elm.style.border="2px solid red";
                    elm.style="";""".format(css=css_selector)
        self.run_js(js)

    def window_scroll(self, width=None, height=None):
        """
        JavaScript API
        设置窗口滚动条的高度和宽度，一般只需要设置height

        Usage:
        driver.window_scroll(height=500)
        """
        if width is None:
            width = "0"
        if height is None:
            height = "0"
        js = "window.scrollTo({w},{h});".format(w=width, h=height)
        self.run_js(js)

    def move_mouse(self, x, y):
        """
        移动鼠标到一个指定的坐标

        Usage:
        driver.move_mouse(200, 200)
        """
        ActionChains(self.driver).move_by_offset(x, y).perform()

    def element_is_exist(self, css):
        """
        判断元素是否存在，存在返回True，不存在返回False

        Usage：
        driver.element_is_exist("#el")
        """
        try:
            self.get_element(css)
        except:
            return False
        else:
            return True
