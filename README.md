Scu-ncov-auto
====
解决微服务健康打卡系统2.0增加的六位验证码阻挡机器人的问题，实现自动打卡
----
# 免责声明：
## 本项目仅供学习交流使用，请勿用于其他用途！
## 根据《教育部公安厅关于进一步做好新型冠状病毒感染的肺炎疫情“日报告、零报告”工作的通知》、《中华人民共和国传染病防疫法》、《中华人民共和国治安管理处罚法》等，请需要打卡的同学于每天中午12:00前通过“健康每日报”功能进行每日健康打卡，在填写过程中确认真实无误，若有任何问题，请及时与辅导员联系！

# 隐私声明：
## 您输入的所有数据（包括但不限于学号、密码、地理位置信息）均储存在您本人的计算机或服务器上，仅用于微服务身份认证，不会以任何形式泄露！

# 本项目可实现：
* 使用账号密码自动登录
  * 无需提供cookies，无需担心cookies失效问题
  * 可实现批量打卡
* 继承上次打卡数据，自动填报
  * 无需获取post表单中uid、id等信息
* 根据提供的经纬度信息虚拟获取位置
  * 解决部分设备或浏览器无定位功能的问题

# 使用方法：
## 以应用程序运行：
确保有chrome浏览器，并[在此](http://npm.taobao.org/mirrors/chromedriver/)下载对应版本的chromedriver <br>
将chromedriver.exe放入tools目录 <br>
在腾讯云开放平台，注册账号获取app_id, app_key,
# 薅腾讯的羊毛，它不香吗？（doge）

## 以python文件运行：
确保有chrome浏览器，并[在此](http://npm.taobao.org/mirrors/chromedriver/)下载对应版本的chromedriver <br>
将chromedriver.exe放入tools目录 <br>
更改ncov.py中学号、密码、纬度、经度信息
```
python ncov.py
```

# 开发 & 更新：
author: Jeffery <br>
e-mail: lp1559345469@gmail.com <br>
使用python - selenium开发 <br>
持续更新，可通过邮箱反馈问题、提出建议、催更 <br>
#### 请留下star，谢谢！

