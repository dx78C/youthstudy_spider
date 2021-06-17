import requests
import re
import bs4
from bs4 import BeautifulSoup
import os
import smtplib
import glob as gb  # 导入glob模块
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import json
from lxml import etree
import shutil
headers = {
    'user - agent': 'Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 80.0.3987.116Safari / 537.36'
}
DATAFILENAME = "data.json"  # 数据文件的名称


def get_first_url(url):  # 得到第一个url，即每一篇文章的url，结果是未遍历的

    res_1 = requests.get(url=url, headers=headers)
    html_1 = res_1.text

    first_url = re.findall('<li.*?<a.*?"(//w.*?search)"', html_1, re.S)
    # first_url = re.findall('<li.*?<a.*?"(//www.bilibili.com/read/cv*)"', html_1, re.S)
    return first_url


# 获取下载链接
def get_second_url(url):  # 得到第二个url，即文章中每个图片的url，结果是未遍历的
    res_2 = requests.get(url=url, headers=headers)
    html_2 = res_2.text
    soup = bs4.BeautifulSoup(html_2, 'html.parser')
    picture_list = soup.select('.img-box img')
    soup = BeautifulSoup(html_2, 'lxml')
    title='title = {}'.format(soup.find_all('title'))

    str1 = '第'
    str2 = '期'
    try:
        start = title.index(str1);
        end = title.index(str2);
    except:
        print("err")
    title=title[start:end + 1]
    print(title)

    return picture_list, title


# 下载图片
def download_picture(title, url, dir, num1, i):
    res_3 = requests.get(url=url, headers=headers)
    picture_data = res_3.content
    #  picture_name = 'img{}_{}.jpg'.format(num1, i)
    picture_name = title + str(i) + '.jpg'
    picture_path = dir + picture_name
    with open(picture_path, 'wb') as f:
        f.write(picture_data)


# 发送邮件
# https://www.jianshu.com/p/f6ac9e997ef5
def sendEmail(dataGroup, title):
    # 定义相关数据,请更换自己的真实数据
    smtpserver = dataGroup["smtpserver"]
    sender = dataGroup["sender"]
    receiver = dataGroup["receiver"]
    username = dataGroup["username"]
    password = dataGroup["password"]

    msg = MIMEMultipart()

    msg['Subject'] = Header(title, 'utf-8')
    msg['From'] = sender
    receivers = receiver
    print(title,'\n',"发送方:",sender,"\n","接收方:",receivers)
    toclause = receivers.split(',')
    msg['To'] = ",".join(toclause)
    # print("send email:",msg['To'])
    i = 0

    img_path = gb.glob(dataGroup["dir"] + "*.jpg")
    #'"""' +
    body ='<h1>共' + str(len(img_path)) + '张图片</h1></br>'
    for path in img_path:
        imgId = 'image' + str(i)
        fp = open(path, 'rb')
        images = MIMEImage(fp.read())
        fp.close()
        images.add_header('Content-ID', imgId)
        msg.attach(images)
        # body = body + '<img src="cid:' + imgId + '">'
        i += 1
    # body = body + \
    #        '"""'
    mail_body = MIMEText(body, _subtype='html', _charset='utf-8')
    msg.attach(mail_body)

    # 登陆并发送邮件
    try:
        smtp = smtplib.SMTP()
        ##打开调试模式
        # smtp.set_debuglevel(1)
        smtp.connect(smtpserver)
        smtp.login(username, password)
        smtp.sendmail(sender, toclause, msg.as_string())
    except:
        print("邮件发送失败！！")
    else:
        print("邮件发送成功")
    finally:
        smtp.quit()


def haveDataFile():
    path = os.getcwd()
    filelist = os.listdir(path)
    for file in filelist:
        if file == DATAFILENAME:
            return True
    return False

#
# https://blog.csdn.net/qq_44921056/article/details/113398597
if __name__ == '__main__':
    if haveDataFile() == False:
        print("[{}]".format(time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime())), "未读取到数据，新建数据文件,请到目录下的data.json配置信息")
    else:
        dataFile = open(DATAFILENAME, "rb")
        dataGroup = json.load(dataFile)
        dataGroup = dataGroup[1]
        # 创建文件夹
        dir = dataGroup["dir"]
        if os.path.exists(dir):
            shutil.rmtree(dir)  # 将整个文件夹删除
        os.mkdir(dir)

        base_url = 'https://search.bilibili.com/article?keyword='
        # insert=input()
        insert = '青年大学习'
        #+'&from_source=webhistory_search'
        base_url = base_url + insert
        fist_urls = get_first_url(base_url)

        # num1 = 1
        first_url = 'https:' + fist_urls[0]
        second_url, title = get_second_url(first_url)
        user = dataGroup["user"]
        title = user + title
        for i in range(len(second_url)):
            picture_urls = second_url[i].get('data-src')
            picture_url = 'https:' + picture_urls
            download_picture(title, picture_url, dir, 1, i)
        # num1 += 1
        sendEmail(dataGroup, title)
