import smtplib
from email.mime.text import MIMEText
from email.header import Header
sender = "1559345469@qq.com"
receivers = ["1559345469@qq.com",]
message = MIMEText("Test")
message["from"] = Header("Test", "utf-8")
message["To"] = Header("Test", "utf-8")
subject = "git actions test"
message["Subject"] = Header(subject, "utf-8")

mail_host="smtp.qq.com"  #设置服务器
mail_user="1559345469@qq.com"    #用户名
mail_pass="imxlmszvzwnlhbej"   #口令 

smtp = smtplib.SMTP() 
smtp.connect(mail_host, 25)    # 25 为 SMTP 端口号
smtp.login(mail_user,mail_pass)  
smtp.sendmail(sender, receivers, message.as_string())
