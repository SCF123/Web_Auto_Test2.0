import configparser
import os, shutil
from selenium_lib.weblog import MyLog
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import smtplib


logger = MyLog().get_logger()


# Tip: 在PyCharm中创建ini格式的文件选择对应的文件类型, setting–>marketplace 搜索Ini4Idea ，然后进行安装，重启PyCharm即可。
# function: 封装读取配置文件web_auto.ini的接口
class Readconfig(object):
    def __init__(self):
        self.conf_path = os.path.join(
            os.path.split(os.path.realpath(__file__))[0][:-12],
            "web_auto.ini"
        )
        self.cf = configparser.ConfigParser()
        self.cf.read(self.conf_path, encoding="utf-8")

    def get_value(self, section, option):
        if self.cf.has_section(section):
            if self.cf.has_option(section, option):
                value = self.cf.get(section, option)
                return value

        logger.error("读取配置失败! section->{}, option->{}\n "
                     "   配置文件路径：{}".format(section, option,self.conf_path), exc_info=True)
        return None


# 发送通知邮件
def send_mail(text, file):
    sender = Readconfig().get_value('Email', 'sender')
    receiver = Readconfig().get_value('Email', 'receiver')
    subject = Readconfig().get_value('Email', 'subject')
    smtpserver = Readconfig().get_value('Email', 'smtpserver')
    password = Readconfig().get_value('Email', 'password')

    # 组装邮件标题和内容
    msg = MIMEMultipart()
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = receiver

    # 邮件正文内容
    msg.attach(MIMEText(text, 'plain', 'utf-8'))

    fp = None
    try:
        fp = open(file, 'rb')
    except FileNotFoundError:
        logger.error("此文件路径有误 {} ！".format(file), exc_info=True)
        exit()
    # 构造附件，传送新生成的测试报告
    attachment = MIMEText(fp.read(), 'base64', 'utf-8')
    attachment["Content-Type"] = 'application/octet-stream'
    # 这里的filename即邮箱中显示的附件名，理论可以随便设置
    # 我这里依然使用原文件名，可以用file[-35:]从文件路径中截取
    attachment["Content-Disposition"] = 'attachment; filename="' + file[-35:] + '"'
    msg.attach(attachment)

    # 登录并发送邮件
    smtp = smtplib.SMTP()
    try:
        smtp.connect(smtpserver)
        smtp.login(sender, password)
        smtp.sendmail(sender, msg['To'].split(";"), msg.as_string())
        logger.info('邮件发送成功！')
        # print("邮件发送成功！")
    except:
        logger.error('邮件发送失败', exc_info=True)
        # print("邮件发送失败！")
    finally:
        smtp.quit()
        fp.close()


def skip_testcase():
    # 读取配置文件中添加的不执行的用例文件
    notruncase = Readconfig().get_value("NotRunCase", "case")
    notcase = notruncase.split(";")

    path = os.path.split(os.path.realpath(__file__))[0][:-12]
    notruncase_path = os.path.join(path, "testcase\\notruncase")
    runcase_path = os.path.join(path, "testcase")
    
    notrun_cases = os.listdir(notruncase_path)
    run_cases = os.listdir(runcase_path)

    # 启用之前不执行的用例，将其从notruncase文件夹移动到testcase文佳夹
    for not_runcase in [case for case in notrun_cases if case not in notcase]:
        if not_runcase is None:
            break
        shutil.move(os.path.join(notruncase_path, not_runcase), runcase_path)

    # 不执行配置的用例文件，将不执行的用例移动到notruncase
    for case_file in [case for case in notcase if case in run_cases]:
        if case_file is None:
            break
        shutil.move(os.path.join(runcase_path, case_file), notruncase_path)


# 测试代码
if __name__ == "__main__":
    # 测试邮件发送功能
    # filename = 'C:\\Users\\11848\\Desktop\\会议材料\\New_UITest\\result\\testreport\\test.txt'
    # text = "最新Web自动化测试报告请接收，见附件。"
    # send_mail(text, filename)
    
    # 测试配置文件读取功能
    val = Readconfig().get_value("PlatForm", "account")
    print(val)

    # skip_testcase()
