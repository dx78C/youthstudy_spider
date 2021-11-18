# 🚀️ youthstudy_spider

> 使用者有责任和义务对自己的行为负责。  
> 本项目仅供学习交流使用，严禁用于其他用途! For learning and communication only, other use is strictly prohibited！  
> 作者不承担任何法律责任！The author assumes no legal liability！  

青年大学习爬虫：获取最新完成页面，并发到指定邮箱。  
配合自动学习脚本（<https://github.com/CNawalol/qndxx-action>）可以全程自动完成

## 🎉️ 使用方法
data.json中将下面配置信息填写在对应下方大括号内：
```
"user": "学号+姓名+",
"dir": "下载目录",
"smtpserver": "邮箱smtp服务器",
"sender": "发送邮箱",
"password": "授权码",
"receiver": "接收邮箱1,接收邮箱2",
"username": "登录邮箱"
```

### 方法一：window程序运行👑

1.下载exe程序 <https://github.com/Colflip/youthStudy/releases>

2.配置data.json文件 

3.运行exe文件

（可以设置定时计划，需要将data文件其放入C:\Windows\System32 ）


### 方法二：python运行

1.配置data.json文件  

2.运行main.py  


## 🎈注意说明

### ⚡不能在代理网络下使用  

### ⚡QQ邮箱smtp服务器配置：  
![img.png](img/img1.png)  

QQ获取邮箱授权码:  
![img.png](img/img2.png)  

## ❤ 感谢  
[QiYi92](https://github.com/QiYi92/Youth_Learning_Reptile)  
[zhouyumin](https://github.com/zhouyumin/qndxx)

## python打包exe
pyinstaller -F main.py
