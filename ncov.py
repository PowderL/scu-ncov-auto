# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header
# sender = "1559345469@qq.com"
# receivers = ["1559345469@qq.com",]
# message = MIMEText("Test")
# message["from"] = Header("Test", "utf-8")
# message["To"] = Header("Test", "utf-8")
# subject = "git actions test"
# message["Subject"] = Header(subject, "utf-8")

# mail_host="smtp.qq.com"  #设置服务器
# mail_user="1559345469@qq.com"    #用户名
# mail_pass=""   #口令 

# smtp = smtplib.SMTP() 
# smtp.connect(mail_host, 25)    # 25 为 SMTP 端口号
# smtp.login(mail_user,mail_pass)  
# smtp.sendmail(sender, receivers, message.as_string())
# -*- coding: UTF-8 -*-

"""
author: Aaron
e-mail: w98987@126.com
wechat official account: 化院学生从不学化学
"""

import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sys
class Clock:
    def __init__(self):
        self.target = 'https://wfw.scu.edu.cn/ncov/wap/default/index'  # 微服务地址
        self.url = 'https://ua.scu.edu.cn/login'
        self.username = ''  # 用户名
        self.password = ''  # 密码
        self.lat = 0  # 维度
        self.long = 0  # 经度

    def main(self):
        print('preparing...')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome('./tools/chromedriver.exe', options=chrome_options)
        print('working...')
        browser.delete_all_cookies()  # 清空cookie
        browser.get(self.target)
        try:  # 切换为账号密码登录
            browser.switch_to.frame('loginIframe')  # 切换frame
            switch_element = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[2]/div[2]/div[1]/div/div[3]'))
            )
            switch_element.click()
        except Exception as error:
            print('network wrong...\n', error)
        input_element = browser.find_elements_by_tag_name('input')
        username_element, password_element = input_element[0], input_element[1]
        username_element.send_keys(self.username)  # 填用户名
        password_element.send_keys(self.password)  # 填密码
        browser.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/div[2]/div[3]/button').click()  # 点击登录
        time.sleep(1)  # 等待跳转
        browser.execute_cdp_cmd(
            "Browser.grantPermissions",  # 授权地理位置信息
            {
                "origin": "https://wfw.scu.edu.cn/",
                "permissions": ["geolocation"]
            },
        )
        browser.execute_cdp_cmd(
            "Emulation.setGeolocationOverride",  # 虚拟位置
            {
                "latitude": self.lat,
                "longitude": self.long,
                "accuracy": 50,
            },
        )
        try:  # 提交位置信息
            area_element = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.NAME, 'area'))
            )
            area_element.click()
        except Exception as error:
            print('get location wrong...\n', error)
        time.sleep(1)  # 等待位置信息
        browser.find_element_by_xpath('/html/body/div[1]/div/div/section/div[5]/div/a').click()  # 提交信息
        try:
            ok_element = WebDriverWait(browser, 3).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]/div[2]'))  # 提交按钮
            )
            ok_element.click()
            print(self.username, 'success!')
            WebDriverWait(browser, 3).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div[1]'))  # 成功对话框标题
            )
            title_success = browser.find_element_by_xpath('/html/body/div[5]/div/div[1]').get_attribute("innerHTML")
            print('From website:', title_success)
        except:
            info = browser.find_element_by_class_name('wapat-title').get_attribute('innerHTML')
            print('From website:', self.username, ':', info)
        browser.quit()


if __name__ == '__main__':
    x = Clock()
    x.main()
