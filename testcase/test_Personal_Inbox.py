"""
用例作者：scf
用例明细：
    test_asend_message(self):[个人信息]--[收件箱]，验证发送消息功能
    test_query_message(self):[个人中心]--根据条件查询消息
    test_view_message(self):[个人消息]--查看消息
    test_reply_message(self):[个人消息]--回复收到的消息
    test_mark_message(self):[个人消息]--标记消息
    test_zdel_message(self):[个人消息]--删除收件箱和发件箱中的消息
"""

from selenium_lib import Pyse, TestCase, TestRunner
from testcase.common import platform_api


class Test_Personal_Inbox(TestCase):
    def add_account(self, account_name, account_code):
        """新增一个账号"""
        self.click("xpath=>//span[contains(.,'消息测试组织')]")
        self.click(".mt16 > span")
        self.sleep(1)
        self.clear("xpath=>(//input[@type='text'])[5]")
        self.type("xpath=>(//input[@type='text'])[5]", account_name)
        self.clear("xpath=>(//input[@type='text'])[6]")
        self.type("xpath=>(//input[@type='text'])[6]", account_code)
        # 勾选组织 消息测试组织
        org_elements = self.get_elements(".ivu-row:nth-child(3) > .ivu-col:nth-child(1) .ivu-tree > .ivu-tree-children")
        for i in range(2, len(org_elements) + 2):
            org_name = self.get_text(
                f".ivu-row:nth-child(3) > .ivu-col:nth-child(1) .ivu-tree > "
                f".ivu-tree-children:nth-child({i}) .ivu-tree-listItem .ivu-tree-title"
            )
            if "消息测试组织" == org_name:
                self.click(
                    f".ivu-row:nth-child(3) > .ivu-col:nth-child(1) .ivu-tree > "
                    f".ivu-tree-children:nth-child({i}) .ivu-tree-listItem .ivu-checkbox-input"
                )
                break

        # 勾选角色 消息测试角色
        role_elements = self.get_elements(
            ".ivu-row:nth-child(3) > .ivu-col:nth-child(2) .ivu-tree > .ivu-tree-children")
        for i in range(2, len(role_elements) + 2):
            role_name = self.get_text(
                f".ivu-row:nth-child(3) > .ivu-col:nth-child(2) .ivu-tree > "
                f".ivu-tree-children:nth-child({i}) .ivu-tree-listItem .ivu-tree-title"
            )
            if "消息测试角色" == role_name:
                self.click(
                    f".ivu-row:nth-child(3) > .ivu-col:nth-child(2) .ivu-tree > "
                    f".ivu-tree-children:nth-child({i}) .ivu-tree-listItem .ivu-checkbox-input"
                )
                break
        # 确定提交
        self.click(".item-break-all:nth-child(6) .ivu-btn:nth-child(2) > span")

    def del_account(self, ac_name):
        """删除一个账号"""
        num_1 = len(self.get_elements("#tr_Root_undefined"))
        for i in range(1, num_1 + 1):
            account_name = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/span)[{i}]")
            if ac_name == account_name:
                self.click(f"#tr_Root_undefined:nth-child({i}) .ivu-checkbox-input")
                break
        self.click(".ml0:nth-child(2) > span")
        self.sleep(2)
        self.click(".act-container > div:nth-child(3) .ivu-btn:nth-child(1) > span")
        # 对偶现的删除失败进行处理
        if "删除成功！" != self.get_text(".ivu-message span"):
            self.F5()
            platform_api.open_page(self, 2, "账号管理")
            num_2 = len(self.get_elements("#tr_Root_undefined"))
            for i in range(1, num_2 + 1):
                account_name = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/span)[{i}]")
                if ac_name == account_name:
                    self.click(f"#tr_Root_undefined:nth-child({i}) .ivu-checkbox-input")
                    break
            self.click(".ml0:nth-child(2) > span")
            self.sleep(2)
            self.click(".act-container > div:nth-child(3) .ivu-btn:nth-child(1) > span")
        self.sleep(1)

    def open_personal_info(self):
        """打开个人信息页面"""
        self.sleep(1)
        self.F5()
        self.click(".icon-message")
        self.sleep(1)

    @classmethod
    def setUpClass(cls):
        cls.driver = Pyse("chrome")
        cls.driver.maximize_window()
        platform_api.login_platform(cls.driver)

    def test_asend_message(self):
        """[个人信息]--[收件箱]，验证发送消息功能"""

        # 测试数据准备，建造两个测试账号
        # 先进入[人员管理]-[组织管理]页面创建一个测试组织
        platform_api.open_page(self, 2, "组织管理")
        # 新建一个组织
        self.click(".mr10:nth-child(6) > span")
        self.sleep(1)
        self.clear("xpath=>(//input[@type='text'])[4]")
        self.type("xpath=>(//input[@type='text'])[4]", "消息测试组织")
        self.clear("xpath=>(//input[@type='text'])[5]")
        self.type("xpath=>(//input[@type='text'])[5]", "900211")
        self.click(".dpt-model:nth-child(3) .ivu-btn-primary > span")
        # 关闭组织管理页面
        self.move_to_element(".icon-chuyidong")
        self.click(".icon-shibai")

        # 再进入[人员管理]-[角色管理]页面创建一个测试角色
        platform_api.open_page(self, 2, "角色管理")
        # 新建一个测试角色
        self.click(".float > span")
        self.clear("xpath=>//input[@type='text']")
        self.type("xpath=>//input[@type='text']", "消息测试角色")
        self.click(".role-left > div:nth-child(3) .ivu-btn:nth-child(1) > span")
        # 关闭角色管理页面
        self.move_to_element(".icon-chuyidong")
        self.click(".icon-shibai")

        # 再进入[人员管理]-[账号管理]页面创建一个测试账号
        platform_api.open_page(self, 2, "账号管理")
        self.add_account("消息测试账号1", "message1")
        self.sleep(2)
        self.add_account("消息测试账号2", "message2")
        self.sleep(1)

        # 最后进入[个人中心]页面，给新建的两个账号发送消息
        self.open_personal_info()
        # 切到发件箱获取已发消息数量
        self.click(".ivu-tabs-tab:nth-child(3) > span:nth-child(1)")
        num = self.get_text(".tb-InfoDiv:nth-child(1) .ivu-page-total")
        index_1 = int(num.split(" ")[1])
        # 获取已有收件数量
        self.sleep(1)
        self.click(".ivu-tabs-tab:nth-child(2) > span:nth-child(1)")
        num1 = self.get_text("xpath=>//div[2]/div[3]/ul/span")
        index = int(num1.split(" ")[1]) + index_1

        self.click(".tb-InfoDiv:nth-child(2) .ivu-btn-primary > span")
        self.sleep(1)
        # 选择收件人
        self.click("xpath=>(//input[@type='text'])[18]")
        self.sleep(1)
        num = len(self.get_elements("xpath=>//tr[@id='tr_Root_undefined']/td[2]/div/span"))
        for i in range(1, num+1):
            text = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/span)[{i}]")
            account = ["超级管理员", "消息测试账号1", "消息测试账号2"]
            if text in account:
                self.click(f"xpath=>(//tr[@id='tr_Root_undefined']/td/div/label/span/input)[{i+index}]")
        self.click(".modal-nopadding:nth-child(10) .ivu-modal-footer .ivu-btn-primary")
        # 填写主题
        self.clear("xpath=>(//input[@type='text'])[19]")
        self.type("xpath=>(//input[@type='text'])[19]", "测试给多人发消息")
        # 填写消息正文内容
        self.clear("#msg_content2")
        self.type("#msg_content2", "Hello, everyone!")
        # 确定
        self.click(".modal-nopadding:nth-child(9) .ivu-btn-primary > span")

        # 验证消息是否发送成功
        self.sleep(2)
        self.click(".ivu-tabs-tab:nth-child(3) > span:nth-child(1)")
        send_num = len(self.get_elements("xpath=>//tr[@id='tr_Root_undefined']/td[2]/div/a"))
        messages = []
        for i in range(1, send_num+1):
            message = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/a)[{i}]")
            messages.append(message)
        self.assertIn("测试给多人发消息", messages)

    def test_query_message(self):
        """[个人中心]--根据条件查询消息"""
        self.open_personal_info()

        # 切到发件箱获取已发消息数量
        self.click(".ivu-tabs-tab:nth-child(3) > span:nth-child(1)")
        num = self.get_text(".tb-InfoDiv:nth-child(1) .ivu-page-total")
        index = int(num.split(" ")[1])
        # 切回收件箱
        self.sleep(1)
        self.click(".ivu-tabs-tab:nth-child(2) > span:nth-child(1)")

        # 消息状态：未读
        self.click(".w200 .ivu-icon-ios-arrow-down")
        self.sleep(0.5)
        self.click(".w200 .ivu-select-item:nth-child(2)")
        # 消息标题：测试
        self.clear("xpath=>(//input[@type='text'])[5]")
        self.type("xpath=>(//input[@type='text'])[5]", "测试")
        # 消息来源：超级管理员
        self.clear(".ivu-row:nth-child(2) > .ivu-col:nth-child(2) .ivu-input")
        self.type(".ivu-row:nth-child(2) > .ivu-col:nth-child(2) .ivu-input", "超级管理员")
        # 查询
        self.click(".tb-InfoDiv:nth-child(2) .search .mr10 > span")

        # 验证查询结果是否正确
        self.sleep(1)
        title = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/a)[{index+1}]")
        self.assertIn("测试", title)
        source = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[3]/div/span)[{index+1}]")
        self.assertEqual("超级管理员", source)
        status = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[4]/div/span)[{index+1}]")
        self.assertEqual("未读", status)
        self.sleep(1)

    def test_view_message(self):
        """[个人消息]--查看消息"""
        self.open_personal_info()

        # 切到发件箱获取已发消息数量
        self.click(".ivu-tabs-tab:nth-child(3) > span:nth-child(1)")
        num = self.get_text(".tb-InfoDiv:nth-child(1) .ivu-page-total")
        index = int(num.split(" ")[1])
        # 切回收件箱
        self.sleep(1)
        self.click(".ivu-tabs-tab:nth-child(2) > span:nth-child(1)")

        # 查看并验证接收到的消息
        self.click(f"xpath=>(//tr[@id='tr_Root_undefined']/td[2]/div/a)[{index+1}]")
        self.sleep(1)
        sender = self.get_attribute("xpath=>(//input[@type='text'])[10]", "value")
        self.assertEqual("超级管理员", sender)
        title = self.get_attribute("xpath=>(//input[@type='text'])[11]", "value")
        self.assertEqual("测试给多人发消息", title)

    def test_reply_message(self):
        """[个人消息]--回复收到的消息"""
        self.open_personal_info()

        # 切到发件箱获取已发消息数量
        self.click(".ivu-tabs-tab:nth-child(3) > span:nth-child(1)")
        num = self.get_text(".tb-InfoDiv:nth-child(1) .ivu-page-total")
        index = int(num.split(" ")[1])
        # 切回收件箱
        self.sleep(1)
        self.click(".ivu-tabs-tab:nth-child(2) > span:nth-child(1)")

        # 回复消息
        self.sleep(1)
        self.click(f"xpath=>(//tr[@id='tr_Root_undefined']/td/div/label/span/input)[{index+1}]")
        self.click(".tb-InfoDiv:nth-child(2) .mr10:nth-child(2) > span")
        self.sleep(1)
        self.type("#msg", "ok!")
        self.click(".modal-nopadding:nth-child(8) .ivu-btn-primary > span")

        # 验证回复消息是否成功
        text = self.get_text(".ivu-message span")
        self.assertEqual(text, "发送消息成功！")

    def test_mark_message(self):
        """[个人消息]--标记消息"""
        self.open_personal_info()

        # 切到发件箱获取已发消息数量
        self.click(".ivu-tabs-tab:nth-child(3) > span:nth-child(1)")
        num = self.get_text(".tb-InfoDiv:nth-child(1) .ivu-page-total")
        index = int(num.split(" ")[1])
        # 切回收件箱
        self.sleep(1)
        self.click(".ivu-tabs-tab:nth-child(2) > span:nth-child(1)")

        # 选中消息，查看其状态，如若未读，则执行标记已读操作，否则反之
        self.sleep(1)
        status = self.get_text(f"xpath=>(//tr[@id='tr_Root_undefined']/td[4]/div/span)[{index + 1}]")
        if "未读" == status:
            self.click(f"xpath=>(//tr[@id='tr_Root_undefined']/td/div/label/span/input)[{index + 1}]")
            self.click(".mr10:nth-child(4) > span")
            text = self.get_text(".ivu-message span")
            self.assertEqual(text, "标记已读成功！")
            self.sleep(2)
            self.click(f"xpath=>(//tr[@id='tr_Root_undefined']/td/div/label/span/input)[{index + 1}]")
            self.click(".mr10:nth-child(3) > span")
            text = self.get_text(".ivu-message span")
            self.assertEqual(text, "标记未读成功！")
            self.sleep(1)

        if "已读" == status:
            self.click(f"xpath=>(//tr[@id='tr_Root_undefined']/td/div/label/span/input)[{index + 1}]")
            self.click(".mr10:nth-child(3) > span")
            text = self.get_text(".ivu-message span")
            self.assertEqual(text, "标记未读成功！")
            self.sleep(2)
            self.click(f"xpath=>(//tr[@id='tr_Root_undefined']/td/div/label/span/input)[{index + 1}]")
            self.click(".mr10:nth-child(4) > span")
            text = self.get_text(".ivu-message span")
            self.assertEqual(text, "标记已读成功！")
            self.sleep(1)

    def test_zdel_message(self):
        """[个人消息]--删除收件箱和发件箱中的消息"""
        self.open_personal_info()

        # 先删除发件箱消息
        self.click(".ivu-tabs-tab:nth-child(3) > span:nth-child(1)")
        self.sleep(1)
        # 删除全部消息
        self.click("input.ivu-checkbox-input")
        self.click(".tb-InfoDiv:nth-child(1) .btns .ivu-btn-ghost > span")
        self.sleep(1)
        self.click("div:nth-child(12) .ivu-btn-primary > span")
        self.sleep(2)

        # 再切到收件箱删除消息
        self.click(".ivu-tabs-tab:nth-child(2) > span:nth-child(1)")
        self.sleep(1)
        # 删除全部消息
        self.click("xpath=>//div[2]/div[2]/div/div/div/table/thead/tr/th/div/label/span/input")
        self.click(".mr10:nth-child(5)")
        self.sleep(1)
        self.click("div:nth-child(11) .ivu-btn-primary > span")
        self.sleep(2)

        # 清除组织、角色和账号信息
        platform_api.open_page(self, 2, "账号管理")
        self.del_account("消息测试账号1")
        self.sleep(1)
        self.del_account("消息测试账号2")

        platform_api.open_page(self, 2, "角色管理")
        self.click("xpath=>//span[contains(.,'消息测试角色')]")
        self.click(".role_btn > .del-btn > .icon")
        self.sleep(1)
        self.click("div:nth-child(5) .ivu-btn-primary > span")
        self.sleep(5)

        platform_api.open_page(self, 2, "组织管理")
        self.click("xpath=>//span[contains(.,'消息测试组织')]")
        self.click(".mr10:nth-child(3) > span")
        self.sleep(1)
        self.click(".tenant-model:nth-child(5) .ivu-btn-primary > span")
        self.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    TestRunner().debug()
