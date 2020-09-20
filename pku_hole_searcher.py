from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_email(data, keyword_each):
    mail_host = ""  # 设置服务器
    mail_user = ""  # 用户名
    mail_pass = ""  # 口令

    sender = ''
    receivers = ['']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(data, 'plain', 'utf-8')
    message['From'] = Header("树洞搜索器", 'utf-8')
    message['To'] = Header("就是你", 'utf-8')

    subject = '找到关键字 %s' % keyword_each
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


def get_data(keyword):
    result = []
    global result_pre
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://pkuhelper.pku.edu.cn/hole/")
    time.sleep(0.5)
    box_content = driver.find_elements_by_css_selector("div.flow-item")
    for i in range(len(box_content)):
        s = box_content[i].text.split("#")
        result.append(s[1])
    for i in range(len(result)):
        for keyword_each in keyword:
            if keyword_each in result[i]:
                for each in result_pre:
                    if each == result[i][:6]:
                        print("重复")
                        break
                else:
                    send_email(result[i], keyword_each)
                    result_pre.append(result[i][:6])
                    print(result[i])
    driver.quit()


if __name__ == "__main__":
    result_pre = [""]
    keyword = [""]  # 可填多个关键词
    while 1:
        get_data(keyword)
