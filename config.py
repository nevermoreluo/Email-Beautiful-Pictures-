# -*- coding: utf-8 -*-

#_author = Nevermore_luo

#收件人邮箱地址，群发请用逗号隔开,ex: 'xxxx@qq.com,zzz@126.com' 
To = ''
#发件人邮箱地址 
From='xxx@126.com'
#密码 
Password='546546'
#发件人邮箱的SMTP服务器地址 
#126:'smtp.126.com'\163:'smtp.163.com'\qq:'smtp.qq.com'\sina:'smtp.sina.com'\gmail:'smtp.gmail.com' 
SMTPServer='smtp.126.com'
#邮件标题，适当修改标题，有些标题会被系统判定为垃圾邮件
title = 'Pictures'
#服务器端口 
SMTPPort=25

#图片数量 
Picture_quantity = 10
#是否保存图片，True/False 
Save_pic = True
#保存位置(请务必保留引号前面的r) 
Dirname = r'c:\xxx'
