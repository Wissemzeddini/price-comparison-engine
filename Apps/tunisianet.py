import requests
from bs4 import BeautifulSoup
import mysql.connector
from Apps.sqlQuery import *

class links:  
    def __init__(self, name, link):  
        self.name = name  
        self.link = link 
#this function extract all tunisianet category
def search_catg():
    list=[]
    web = requests.get('https://www.tunisianet.com.tn/').text
    parse = BeautifulSoup(web, 'lxml')
    for c in parse.find_all('div', class_ = 'wb-menu-row'):
        title=c.find_all('li', class_='menu-item item-header')
        for t in title:
            link=t.a['href']
            name=t.a.text
            list.append( links(name, link) )
    return list

#return single page details
def tunisianet_det(url):    
    web = requests.get(url).text
    parse = BeautifulSoup(web, 'lxml')
    try:
        brand_logo=parse.find('div', class_='product-manufacturer').a.img['src']
    except:
        brand_logo='None'
    feautre, titre='',''
    name= parse.find_all('dt', class_='name')
    value = parse.find_all('dd', class_='value')
    fich_list=[]
    for n in name:
        fich_tech={
            'label': n.text,
            'data': ''
            }
        fich_list.append(fich_tech)
    i=0
    for v in value:
        fich_list[i]['feature']=v.text
        i +=1
        
    article={
        'brand_logo':brand_logo,
        'fich_list':fich_list
    }
    return article

def priceConv(price):
    c=''
    for p in price:
        if(p.isdigit()):
            c=c+p
    return int(c)

def next_url(link, x):
    n=''
    if(x==1):
          link=link+'?page='+str(x)
    else:
        link=link[:-1]
        if(x>=10):
            link=link[:-1]
        link=link+str(x)
    text = requests.get(link)
    parse = BeautifulSoup(text.content, 'html.parser')
    nb= parse.find('div', class_='col-md-4 col-lg-4 col-xl-4 hidden-lg-down total-products text-xs-right').p.text
    for c in nb:
        if(c.isdigit()):
            n=n+c
    return link, parse, n

#the main scraping process
def tunisianet_scraping_core(link, info):
    i=0
 #     categorieAdd(name, link, 17)
 #     supCatId=getCagId(name, 17)
    for x in range(1,30):
        link, parse, n = next_url(link, x)
        print(link)
        if(int(n) > i):
            art = parse.find_all('article', class_='product-miniature js-product-miniature col-xs-12 propadding')
            for a in art:
                i=i+1
                try:
                    prod= a.find('h2', class_='h3 product-title').text
                except:
                    prod='Unknown'
                try:
                    img= a.find('img', class_='center-block img-responsive')['src']
                except:
                    img='Undefined'
                try:
                    brand= a.find('img', class_='img img-thumbnail manufacturer-logo')['alt']
                except:
                    brand='Unknown'
                try:
                    price= a.find('span', class_='price').text.replace(u'&nbsp;','')
                    price=priceConv(price)
                except:
                    price=0
                try:
                    uid= a.find('span', class_='product-reference').text.replace('[','').replace(']','')
                except:
                    uid='None'
                try:
                    stock= a.find('span', class_='in-stock').text
                except:
                    stock='Undefined'
                try:
                    des = a.find('div', class_='listds').a.p.text
                except:
                    des= 'None'
                art_link = a.find('h2', class_='h3 product-title').a.get('href')
                det=tunisianet_det(art_link)
#                 brandAdd(brand, det['brand_logo'], 17)
#                 supBrandId=getBrandId(brand ,17)
#                 prodId=AddProduct(prod, art_link, uid, des, price, stock, 17, supBrandId, supCatId, img)
#                 print(price)
#                 if(det['fich_list']):
#                     AddProductAttribut(det['fich_list'], prodId)
                print(prod)
        else:
            break
        
def tunisianet():
    list=search_catg()
    for l in list:
        tunisianet_scraping_core(l.link, l.name)
