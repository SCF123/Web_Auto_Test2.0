from selenium_lib import Readconfig
from selenium_lib.weblog import MyLog
import time, socket, datetime
import requests, json

logger = MyLog().get_logger()


def open_page(driver, menu_index, *child_pages):
    """
    打开一个页面, 此接口只适用于技术开发平台

    :param driver: self
    :param menu_index: 一级菜单索引
    :param child_pages: 二级菜单名称[及下级菜单名称]

    Usage：
    打开 “系统管理->参数配置->基础参数”页面
    open_page(self, 1, "参数配置", "基础参数)
    """
    driver.F5()
    driver.sleep(2)
    driver.move_to_element(f"xpath=>//li[{menu_index}]/div/div[2]")
    for child_page in child_pages:
        driver.click(f"xpath=>//span[contains(.,'{child_page}')]")
        time.sleep(2)
    driver.move_mouse(500, 500)
    driver.sleep(1)


plat_ip = Readconfig().get_value("PlatForm", "ip_address")
plat_account = Readconfig().get_value("PlatForm", "account")
plat_pwd = Readconfig().get_value("PlatForm", "password")
plat_tenent = Readconfig().get_value("PlatForm", "tenement")


# 登录技术开发平台
def login_platform(driver):
    driver.get(f"http://{plat_ip}/#/login")
    driver.find_element_by_css_selector(".ivu-form-item:nth-child(1) .ivu-input").clear()
    driver.find_element_by_css_selector(".ivu-form-item:nth-child(1) .ivu-input").send_keys(plat_account)
    driver.find_element_by_css_selector(".ivu-form-item:nth-child(2) .ivu-input").clear()
    driver.find_element_by_css_selector(".ivu-form-item:nth-child(2) .ivu-input").send_keys(plat_pwd)
    # 判断租户是不是默认的utry，如果不是，则选择配置的租户
    if "utry1" != plat_tenent:
        driver.find_element_by_css_selector(".ivu-icon-ios-arrow-down").click()
        driver.find_element_by_xpath(f"//li[contains(.,'{plat_tenent}')]").click()
    driver.find_element_by_css_selector(".ulogin-btn").click()
    time.sleep(2)


# 退出技术开发平台
def exit_platform(driver):
    driver.move_to_element(".userName")
    time.sleep(2)
    driver.click(".item > span")


# 获取本机IP
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        logger.error("未能获取到本机IP！")
        s.close()
        return
    else:
        s.close()
        return ip


# 比较日期大小
def compare_time(target_time, start_time, end_time):
    """
    比较目标时间是否在开始时间和结束时间之间
    :param target_time: 目标时间
    :param start_time: 开始时间
    :param end_time: 结束时间
    :return: True / False
    """
    if isinstance(target_time, str):
        target_time = datetime.datetime.strptime(target_time, '%Y-%m-%d %H:%M:%S')

    if isinstance(start_time, str):
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

    if isinstance(end_time, str):
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

    if (target_time >= start_time) and (target_time <= end_time):
        return True
    else:
        return False


# 获取子站列表数据
def get_site_menus():
    host_ip = Readconfig().get_value('Eureka', 'ip')
    oam_account = Readconfig().get_value("OAM", "account")
    oam_pwd = Readconfig().get_value("OAM", "password")

    login_url = f"http://{host_ip}/api/user/login"
    para = {
        "username": oam_account,
        "password": oam_pwd,
        "companyId": ""
    }

    header = {
        "Content-Type": "application/json;charset=UTF-8"
    }

    site_menus = {}
    r = requests.post(login_url, data=json.dumps(para), headers=header)
    if 200 == r.status_code and 0 == r.json()["code"]:
        header["token"] = r.json()["data"]["token"]
        url = f"http://{host_ip}/api/subSite/getSiteMenu"

        re = requests.get(url, headers=header)
        if 200 == re.status_code and 0 == re.json()["code"]:
            re_data = re.json()["data"]
            for site_menu in re_data:
                child = site_menu["child"]
                sites = []
                for i in range(len(child)):
                    if "searchPage" == child[i]["type"]:
                        sites.append(child[i]["name"])
                if len(sites) != 0:
                    site_menus[site_menu["name"]] = sites
            return site_menus
        else:
            logger.error("未能获取到子站数据！请检查接口请求是否正确")
            return
    else:
        logger.error("未能获取到token值！请检查配置文件中Eureka和OAM的配置是否正确。")
        return


if __name__ == "__main__":
    data = get_site_menus()
    print(data)
    print(len(data))

