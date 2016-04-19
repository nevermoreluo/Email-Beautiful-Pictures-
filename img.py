# -*- coding: utf-8 -*-
#_author = Nevermore_luo

import requests
from bs4 import BeautifulSoup
import time
import urllib
from PIL import Image
import os
import datetime


def simple_soup(url,cookies=None,timeout=0.001,retry_count=3):
    '''
    url->str:accord with URL standards
    cookies->dict: give cookies if necessary
    timeout->float: avoid the tragedy 's happening again 
    retry_count->int:repeat times if failed
    return->soup if succeed
    
    use requests,bs4 to read HTML,lazy soup for me :)
    '''
    #set headers user_agent,chrome F12
    user_agent = (
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    )
    #repeat if necessary
    for i in range(retry_count):
        try:
            #create session
            session = requests.session()
            session.headers['User-Agent'] = user_agent
            html = session.get(url,cookies=cookies).content
            #normally we dont use this('lxml'),unless system install two version bs4
            soup = BeautifulSoup(html,'lxml')
        except:
            soup = None
        if soup:
            return soup
        #print an error if we got nothing
        print('Alreadly try %s times,but failed, url:%s...'%(i,url))
        #take a break
        time.sleep(timeout)


class Img(object):
    '''
    Pictures searcher:
    get urls(Img.img_urls),download(Img.img_download),
    resize(Img.img_resize,Img.img_resize_all) or delete(Img.img_del)
    
    ex:
        i = Img(n)
        i.img_download(dir)
        i.img_resize_all(size=(510,765),del=True)
    '''
    def __init__(self,n):
        '''
        n->int:pictures number
        '''
        
        #base url all pictures from this URL
        self.url = 'http://www.topit.me/?p='
        #get cookies from topit with chrome, it seems last forever lucky :)
        self.cookies = {
        'Hm_lpvt_5256b9d21d9d68644fca1a0db29ba277': '1460191049',
        'Hm_lvt_5256b9d21d9d68644fca1a0db29ba277': '1460182034,1460187743,1460191049',
        'PHPSESSID': 'asf1i64794v93ng53b2ppup4j7',
        '__utma': '137188917.367896211.1460182035.1460187062.1460190197.3',
        '__utmb': '137188917.3.10.1460190197',
        '__utmc': '137188917',
        '__utmt': '1',
        '__utmz': '137188917.1460182035.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        'is_click': '1',
        'item-tip': 'true',
        'tip_global_1': 'true'
        }
        #how many pictures do we want
        self.n = n
    
    
    def _img_url_seach(self,url):
        soup = simple_soup(url,cookies=self.cookies)
        #get item_id from topit
        temp = [i.img['id'].split('_')[-1] 
                for i in soup.find_all('div',{'class':'e m'})]
        phurl = 'http://www.topit.me/item/'
        #use item_id make topit urls about pictures
        topit_url = [''.join((phurl,u)) for u in temp]
        return topit_url
        
    
    def img_urls(self):
        '''
        return -> list:
        get an list of image urls
        '''
        x, l = 1, []
        #acquire enough pictures
        while len(l) < self.n:
            url = ''.join((self.url,str(x)))
            l += self._img_url_seach(url)
            x += 1
        
        #cut the length we needed
        url_list = l[:self.n]
        self.png_urls = []
        #get pictures urls
        for a,b in enumerate(url_list):
            soup = simple_soup(b,cookies=self.cookies)
            item_id = ''.join(('item_d_',b.split('/')[-1]))
            print(b)
            png = soup.find('img',{'id':item_id})['src']
            self.png_urls.append(png)
        return self.png_urls
        
        
    def img_download(self,dirname=''):
        '''
        dirname -> str:
        return -> None
        download pictures into legal dirname ,
        if dirname doesn't exist create a new one
        '''
        #get urls first
        if not hasattr(self,'png_urls'):
            self.img_urls()
        #if dirname doesn't exist create a new one
        if not os.path.exists(dirname):
            try:
                os.mkdir(dirname)
            except:
                #raise an error when illegal dirname found
                raise RuntimeError('Illegal Dirname plase check it in config!')
        #get today's date
        t = datetime.date.today().strftime("%Y-%m-%d")
        today_count = len([i for i in os.listdir(dirname) if t in i])
        save_name = '-'.join((t,str(today_count))) if today_count else t
        #give each instance different dirname
        name = os.path.join(dirname,save_name)
        os.mkdir(name)
        #create self.name for img_resize,img_resize_all
        self.name = name
        #download
        for n,png in enumerate(self.png_urls):
            path = os.path.join(name,'%s.png'%(n+1))
            urllib.urlretrieve(png,path)
        
        
    def img_del(self,name):
        #remove it if exist
        if os.path.exists(name):
            os.remove(name)
            
    
    def img_resize(self,name,**kw):
        #defult iphone5
        size = kw.pop('size',(640,1136))
        dirname = kw.pop('dirname',self.name)
        del_old = kw.pop('del',False)
        #raise error if kw doesnt exist
        if kw: raise TypeError('extra keywords: %s'%kw)
        path = os.path.join(dirname,name)
        im = Image.open(path)
        out = im.resize(size)
        rename = os.path.join(dirname,'r-%s'%name)
        out.save(rename)
        if del_old:self.img_del(path)
        
        
    def img_resize_all(self,**kw):
        '''
        resize all png which in dirname 
        '''
        size = kw.pop('size',(640,1136))
        dirname = kw.pop('dirname',self.name)
        del_old = kw.pop('del',False)
        if kw: raise TypeError('extra keywords: %s'%kw)
        #get all png
        namelist = [i for i in os.listdir(dirname) 
                        if i.endswith('png')]
        for i in namelist:
            self.img_resize(i,size,del_old)
