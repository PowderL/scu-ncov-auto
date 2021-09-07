# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header
# sender = ""
# receivers = ["",]
# message = MIMEText("Test")
# message["from"] = Header("Test", "utf-8")
# message["To"] = Header("Test", "utf-8")
# subject = "git actions test"
# message["Subject"] = Header(subject, "utf-8")

# mail_host="smtp.qq.com"  #设置服务器
# mail_user=""    #用户名即是邮箱号
# mail_pass=""   #口令 

# smtp = smtplib.SMTP() 
# smtp.connect(mail_host, 25)    # 25 为 SMTP 端口号
# smtp.login(mail_user,mail_pass)  
# smtp.sendmail(sender, receivers, message.as_string())
# -*- coding: UTF-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import base64
import re
from PIL import Image
from io import BytesIO
import sys
import json
import base64
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models
class Clock:
    def __init__(self):
        self.target = 'https://wfw.scu.edu.cn/ncov/wap/default/index'  # 微服务地址
        self.url = 'https://ua.scu.edu.cn/login'
        self.username = ''  # 用户名
        self.password = ''  # 密码
        self.lat = 30  # 纬度所在校区的纬度
        self.long = 103  # 经度，所在校区的经度
        self.app_id = ""
        self.app_key = ""
    def ocr(self, img_path):
        try: 
            cred = credential.Credential(self.app_id, self.app_key) 
            httpProfile = HttpProfile()
            httpProfile.endpoint = "ocr.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = ocr_client.OcrClient(cred, "ap-guangzhou", clientProfile) 

            req = models.GeneralBasicOCRRequest()
            params = {
                "ImageBase64": base64.b64encode(open(img_path, "rb").read()).decode("utf-8")
            }
            req.from_json_string(json.dumps(params))

            resp = client.GeneralBasicOCR(req) 
            return(resp.TextDetections[0].DetectedText)
        except TencentCloudSDKException as err: 
            print("") 
    def get_check_code(self):
        base64_str = self.browser.get_screenshot_as_base64()
        base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
        binary_data = base64.b64decode(base64_data)
        img_data = BytesIO(binary_data)
        picture = Image.open(img_data)
        picture = picture.crop((self.left, self.top, self.right, self.bottom))
        picture.save('./check_code1.png')
        check_code = self.ocr('./check_code1.png')
        return (check_code)
    def log_in(self):
        
        check_code = self.get_check_code()
        input_element = self.browser.find_elements_by_tag_name('input')
        username_element, password_element, check_code_element= input_element[0], input_element[1], input_element[2]
        username_element.send_keys(self.username)  # 填用户名
        
        password_element.send_keys(self.password)  # 填密码
        check_code_element.send_keys(check_code)
        self.browser.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/div[2]/div[3]/button').click()  # 点击登录
        time.sleep(2)
        try:  # 切换为账号密码登录
            self.browser.switch_to.frame('loginIframe')  # 切换frame
            switch_element = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[2]/div[2]/div[1]/div/div[3]'))
            )
            switch_element.click()
        except Exception as error:
            print('network wrong...\n', error)
        time.sleep(1)
        ## try until loging in 
        if len(self.browser.find_elements_by_xpath('/html/body/div[1]/div/div/section/div[5]/div/a')) == 0:
            time.sleep(1)
            self.log_in()
    def main(self):
        print('preparing...')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome('/home/litao/chromedriver', options=chrome_options)
        print('working...')
        self.browser.delete_all_cookies()  # 清空cookie
        self.browser.get(self.target)
        try:  # 切换为账号密码登录
            self.browser.switch_to.frame('loginIframe')  # 切换frame
            switch_element = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[2]/div[2]/div[1]/div/div[3]'))
            )
            switch_element.click()
        except Exception as error:
            print('network wrong...\n', error)
        ##获取验证码
        self.browser.set_window_size(1250, 840)
        time.sleep(2)
        js="window.scrollTo(500,1000)"
        self.browser.execute_script(js)
        ## firstly log in, get the location of check_img for screenshot
        check_img = self.browser.find_elements_by_tag_name("img")[3]
        self.left = check_img.location['x']
        self.top = check_img.location['y']
        self.right = self.left + check_img.size['width']
        self.bottom = self.top + check_img.size['height']
        ## log in 
        self.log_in()
        time.sleep(1)  # 等待跳转
        self.browser.execute_cdp_cmd(
            "Browser.grantPermissions",  # 授权地理位置信息
            {
                "origin": "https://wfw.scu.edu.cn/",
                "permissions": ["geolocation"]
            },
        )
        self.browser.execute_cdp_cmd(
            "Emulation.setGeolocationOverride",  # 虚拟位置
            {
                "latitude": self.lat,
                "longitude": self.long,
                "accuracy": 50,
            },
        )
        try:  # 提交位置信息
            area_element = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.NAME, 'area'))
            )
            area_element.click()
        except Exception as error:
            print('get location wrong...\n', error)
        time.sleep(1)  # 等待位置信息 
        self.browser.find_element_by_xpath('/html/body/div[1]/div/div/section/div[5]/div/a').click()  # 提交信息
        try:
            ok_element = WebDriverWait(self.browser, 3).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]/div[2]'))  # 提交按钮
            )
            ok_element.click()
            print(self.username, 'success!')
            WebDriverWait(self.browser, 3).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div[1]'))  # 成功对话框标题
            )
            title_success = self.browser.find_element_by_xpath('/html/body/div[5]/div/div[1]').get_attribute("innerHTML")
            print('From website:', title_success)
        except:
            info = self.browser.find_element_by_class_name('wapat-title').get_attribute('innerHTML')
            print('From website:', self.username, ':', info)
        self.browser.quit()

if __name__ == '__main__':
    x = Clock()
    x.main()
