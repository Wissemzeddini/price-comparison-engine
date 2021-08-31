import requests
from bs4 import BeautifulSoup
import mysql.connector
from Apps.sqlQuery import *

def alarabia_links():
    alarabia_list=[]
    web = requests.get('https://www.alarabia.com.tn/').content
    parse = BeautifulSoup(web, 'html.parser')
    head= parse.find('ul', class_='sf-menu').find_all('li')
    for h in head:
        link= h.a['href']
        info= h.a.text
        dect={
                 'info':info,
                 'link':link
                 }
        alarabia_list.append(dect)
    return alarabia_list

def priceConv(price):
    c=''
    for p in price:
        if(p.isdigit()):
            c=c+p
    return int(c)

def alarabia_details(link):
    web = requests.get(link)
    parse = BeautifulSoup(web.content, 'html.parser')
    try:
        name= parse.find('div', class_='pb-center-column col-xs-12 col-sm-4').h1.text
    except:
        name= 'None'
    try:
        uid= parse.find('span', itemprop="sku")['content']
    except:
        uid='Undifined'
    try:
        brand_logo = parse.find('img', class_='man_prod').get('src')
    except:
        brand_logo ='Unknown'
    try:
        des = parse.find('div', class_ ='rte align_justify').text.strip()
    except:
        des= 'None'
    try:
        img = parse.find('span', id ='view_full_size').img['src']
    except:
        img='None'
    try:
        price= parse.find('span', id ='our_price_display').text
        price = priceConv(price)
    except:
        price=0
    try:
        stock = parse.find('span', id ='availability_value').text
    except:
        stock= 'non disponible'
    list=[]
    title, feautre ='',''
    try:
        fich_tech= parse.find('table', class_='table-data-sheet').find_all('tr')
        for f in fich_tech:
            title=f.td.text
            feautre= [t.text for t in f.find_all('td')][1]
            fich_dec={
                'label':title,
                'data':feautre
            }
            list.append(fich_dec)
    except:
        list=[]
    details={
        'name':name,
        'uid':uid,
        'brand_logo':brand_logo,
        'des':des,
        'img':img,
        'price':price,
        'stock': stock,
        'fich_tech':list
    }
    return details

def next_url(url, x):
    if(x==1):
        url = url + '#/page-'+str(x)
    else:
        url =url[:-1]
        if(x>10):
            url = url[:-1]
        url = url + str(x)
    return url

def alarabia_scraping_core(link,info):
#     categorieAdd(info, link, 24)
#     supCatId=getCagId(info,24)
    for x in range(1, 10):
        link = next_url(link,x)
        print(link)
        web = requests.get(link)
        parse = BeautifulSoup(web.content, 'html.parser')
        card= parse.find_all('li', class_='ajax_block_product')
        for c in card:
            try:
                det_link= c.find('a', class_='product_img_link')['href']
            except:
                det_link='NO LINKS'
            if(det_link != 'NO LINKS'):
                det=alarabia_details(det_link)  
#                 brandAdd(det['brand_logo'], det['brand_logo'], 24)
#                 supBrandId=getBrandId(det['brand_logo'], 24)
#                 prodId=AddProduct(det['name'], det_link, det['uid'], det['des'], det['price'], det['stock'], 24, supBrandId, supCatId, det['img'])
#                 if(det['fich_tech']):
#                     AddProductAttribut(det['fich_tech'], prodId)
            print(det['name'])
            
def alarabia():
    list = alarabia_links()
    for l in list:
        alarabia_scraping_core(l['link'],l['info'])