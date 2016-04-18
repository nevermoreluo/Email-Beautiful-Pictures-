# -*- coding: utf-8 -*-
import img
import mail
from config import *
import datetime
import os

def pic_find(Picture_quantity,Dirname):
    '''
    获得一个图片地址列表
    '''
    i = img.Img(Picture_quantity)
    urls = i.img_urls()
    if Save_pic: i.img_download(Dirname)
    return urls
        
def send_pic():
    '''
    将图片以html的形式寄出去
    '''
    urls = pic_find(Picture_quantity,Dirname)
    t = ''.join('<p><img src="%s"></p>'%i for i in urls)
    html = '<html><body><h1>Porn</h1>%s</body></html>'%t
    m = mail.Mail(To,From,Password,SMTPServer,SMTPPort)
    m.make_message(html,Type='html')
    m.send()

if __name__ == '__main__':
    send_pic()
