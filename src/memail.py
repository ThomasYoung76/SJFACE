"""
    Function: 
"""
import traceback
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from email.mime.multipart import MIMEMultipart
from conf.settings import *

# 发送邮件(使用非SSL协议发送，端口25号，如163邮箱发送)
def send_mail_not_SSL(subject, content, attach=''):
    """
    发送邮件，不含附件
    :param subject: 主题
    :param content: 内容
    :param attach:  附件地址，为空则不传附件
    :return:
    """
    # 构造MIMEMultipart对象做为根容器
    msg = MIMEMultipart()
    msg['From'] = Header(u'<%s>' % SENDER, 'utf-8')
    msg['To'] = Header(';'.join(RECEIVERS), 'utf-8')
    if 'CC' in globals().keys():
        msg['Cc'] = Header(';'.join(CC), 'utf-8')
    else:
        CC = []
    msg['Subject'] = Header(subject, 'utf-8')

    # 设定纯文本信息
    text_msg = MIMEText(content, 'plain', 'utf-8')
    msg.attach(text_msg)

    # 如果传入附件，则构造附件，读入测试报告文件并格式化
    if attach:
        # file_result = open(attach, 'rb').read()
        # att1 = MIMEText(file_result, 'base64', 'gb2312')
        with open(attach, 'r') as fp:
            file_result = fp.read()
        att1 = MIMEText(file_result, 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="%s"'% attach
        msg.attach(att1)

    # 发送邮件
    smtp = smtplib.SMTP()
    try:
        smtp.connect(MAIL_HOST, 25)     # 25为SMTP端口号,465或者994为SSL协议端口
        smtp.login(MAIL_USER, MAIL_PASSWORD)
        smtp.sendmail(SENDER, RECEIVERS, msg.as_string())
        print(u"发送邮件成功")
    except smtplib.SMTPException as e:
        print(u"Error, 发送邮件失败")
        traceback.print_exc()
    finally:
        smtp.quit()

# 发送邮件(使用SSL协议发送，腾讯企业邮箱)
def send_mail(subject, plain_contant=None, html_contant=None, attach=''):
    """
    发送邮件，可含附件  -- 修改于2018年2月9日 yangshifu，
    :param subject: 主题
    :param plain_contan: 纯文本内容
    :param plain_contant: 纯html内容
    :param attach:  附件地址，为空则不传附件
    :return:
    """
    # 构造MIMEMultipart对象做为根容器
    msg = MIMEMultipart()
    msg['From'] = Header(u'<%s>' % SENDER, 'utf-8')
    msg['To'] = Header(';'.join(RECEIVERS), 'utf-8')
    if 'CC' in globals().keys():
        global CC
        msg['Cc'] = Header(';'.join(CC), 'utf-8')
    else:
        CC = []
    msg['Subject'] = Header(subject, 'utf-8')

    # 添加纯文本信息
    if plain_contant:
        text_msg = MIMEText(plain_contant, 'plain', 'utf-8')
        msg.attach(text_msg)

    # 添加html文本内容，含JS的html可能邮件无法显示
    if html_contant:
        with open(REPORT_PATH, 'r', encoding='utf-8') as html_file:
            html = html_file.read()
            html_msg = MIMEText(html, 'html', 'utf-8')
        msg.attach(html_msg)

    # 如果传入附件，则构造附件，读入测试报告文件并格式化
    if attach:
        with open(attach, 'r', encoding='utf-8') as fp:
            file_result = fp.read()
        att1 = MIMEText(file_result, 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1.add_header('Content-Disposition', 'attachment', filename=('gbk', '', os.path.basename(attach)))
        # att1["Content-Disposition"] = 'attachment; filename="%s"'% attach
        msg.attach(att1)

    # 发送邮件
    try:
        smtp = smtplib.SMTP_SSL(MAIL_HOST, port=465)   # 25为SMTP端口号,465或者994为SSL协议端口
        smtp.login(MAIL_USER, MAIL_PASSWORD)
        smtp.sendmail(SENDER, RECEIVERS + CC, msg.as_string())
        print("发送邮件成功")
    except smtplib.SMTPException:
        print("Error, 发送邮件失败")
        traceback.print_exc()
    finally:
        smtp.quit()

if __name__ == "__main__":
    send_mail('测试邮件', plain_contant=None, attach=REPORT_PATH)