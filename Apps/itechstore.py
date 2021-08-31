import requests
from bs4 import BeautifulSoup
import mysql.connector
import re
from Apps.sqlQuery import *

#get all itechstore links
def itechStore_links():    
    itech_list=[]
    web = requests.get('https://www.itechstore.tn/')
    parse = BeautifulSoup(web.content, 'html.parser')
    itech_links= parse.find_all('a', class_="nav-link")
    i=0
    for it in itech_links:
        i=i+1
        if(i>1 and i<10):
            link=it['href']
            info=it.text.strip()
            tech_dict={
                'link':link,
                'info':info
            }
            itech_list.append(tech_dict)
    return itech_list

#extract details from single page
def tech_details(link):
    web = requests.get(link)
    parse = BeautifulSoup(web.content, 'html.parser')
    try:
        name=parse.find('h1', class_='h1 page-title').text
    except:
        name='Unkonwn'
    try:
        uid= parse.find('div', class_='product-reference').span.text
    except:
        uid='Undifined'
    try:
        stock= parse.find('div', class_='rte-content').p.span.text.replace('!','').strip()
    except:
        stock='non disonible'
    try:
        brand = parse.find('div', class_='product_header_container clearfix').meta['content']
    except:
        brand='Unknown'
    try:
        brand_logo = parse.find('div', class_='product_header_container clearfix').div.a.get('href')
    except:
        brand_logo = 'None'
    try:
        des = parse.find('div', class_='rte-content').text
        des= re.sub(r'(\s+|\n)', ' ', des)
    except:
        des='None'
    label, data='',''
    feautre= parse.find_all('dt', class_='name')
    value = parse.find_all('dd', class_='value')
    fich_list=[]
    for n in feautre:
        fich_tech={
            'label': n.text,
            'data': ''
            }
        fich_list.append(fich_tech)
    i=0
    for v in value:
        fich_list[i]['data']=v.text
        i +=1
    details={
          'name':name, 
          'uid':uid,
          'stock':stock,
          'brand':brand,
          'brand_logo':brand_logo,
          'des':des,
          'fich_list':fich_list
      }
    return details

#multi return function
# return next url page and content page
def next_url(url, x):
    if(x == 1):
        url=url+'?page='+str(x)
    else:
        url=url[:-1]
        if(x>10):
          url=url[:-1]
        url=url+str(x)
    web = requests.get(url)
    parse = BeautifulSoup(web.content, 'html.parser')
    if(parse.find('div', class_='alert alert-warning')):
        return False, parse

    return url, parse

#extract number from string
def priceConv(price):
    c=''
    for p in price:
        if(p.isdigit()):
            c=c+p
    return int(c)

#main scraping process
def itechstore_scraping_core(link, info):
#     categorieAdd(info, link, 20)
#     supCatId=getCagId(info,20)
    for x in range(1,10):
        link, parse = next_url(link,x)
        print(link)
        if(not(link == False)):
            card = parse.find_all('article', class_='product-miniature product-miniature-default product-miniature-grid product-miniature-layout-1 js-product-miniature')
            for c in card:
                art_link= c.find('h3', class_='h3 product-title').a['href']
                try:
                    img= c.find('div', class_='thumbnail-container').a.img.get('data-src')
                except:
                    img='None'
                try:
                    price= c.find('span', class_='product-price').text
                    price=priceConv(price)
                except:
                    price=0
                det= tech_details(art_link)
#                 brandAdd(det['brand'], det['brand_logo'], 20)
#                 supBrandId=getBrandId(det['brand'], 20)
#                 prodId=AddProduct(det['name'], art_link, det['uid'], det['des'], price, det['stock'], 20, supBrandId, supCatId, img)
#                 if(det['fich_list']):
#                     AddProductAttribut(det['fich_list'], prodId)
                print(det['name'])
        else:
            break
                

#scraping multi category
def itech_store():
    list = itechStore_links()
    for l in list:
        itechstore_scraping_core(l['link'], l['info'])


