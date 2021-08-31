import requests
from bs4 import BeautifulSoup
import mysql.connector
from Apps.sqlQuery import *

def spacenet_links():
    list=[]
    web = requests.get('https://spacenet.tn/')
    parse = BeautifulSoup(web.content, 'html.parser')
    head= parse.find_all('div', class_='title title_font')
    for h in head:
        try:
            info= h.find('a').text.strip()
            link= h.find('a').get('href')
        except:
            info= 'None'
            link='None'
        if(info != 'None' ):
            space_dict={
                'info':info,
                'link':link
            }
            list.append(space_dict)
    return list

def priceConv(price):
    c=''
    for p in price:
        if(p.isdigit()):
            c=c+p
    return int(c)

def space_det(url):
    text = requests.get(url).text
    soup = BeautifulSoup(text, 'lxml')
    try:
        name= soup.find('h1', class_ ='h1').text.replace('|','')
    except:
        name = 'Unknown'
    try:
        brand = soup.find('div', class_='product-manufacturer').a.img.get('alt')
        brand_logo = soup.find('div', class_='product-manufacturer').a.img.get('src')
    except:
        brand = 'Unknown'
        brand_logo = 'None'
    try:
        price= soup.find('div', class_ ='current-price').span.text
        price = priceConv(price)
    except:
        price = 0
    try:
        stock = soup.find('div', class_ = 'product-quantities').label.text
    except:
        stock = 'épuise'
    try:
        sku = soup.find('div', class_ = 'product-reference').span.text.strip()
    except:
        sku = 'None'
    try:    
        des = soup.find('div', class_ = 'product-des').p.text.strip()
    except:
        des='None'
    article ={
          'name':name,
          'brand': brand,
          'brand_logo':brand_logo,
          'price': price,
          'stock': stock,
          'sku': sku,
          'des': des,
      }
    return article

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
    if(parse.find('section', class_='page-content page-not-found')):
        return False, parse  

    return url, parse

def spacenet_scraping_core(link, info):
#     categorieAdd(info, link, 23)
#     supCatId=getCagId(info,23)
    for x in range(1,30):
        link, parse= next_url(link,x)
        print(link)
        if(not(link == False)):
            card= parse.find_all('div', class_='item col-xs-12 col-sm-6 col-md-6 col-lg-3')
            for c in card:
                img= c.find('span', class_='cover_image').img['src']
                det_link= c.find('div', class_='product_name').a['href']
                det=space_det(det_link)
#                 brandAdd(det['brand'], det['brand_logo'], 23)
#                 supBrandId=getBrandId(det['brand'], 23)
#                 prodId=AddProduct(det['name'], det_link, det['sku'], det['des'], det['price'], det['stock'], 23, supBrandId, supCatId, img)
                print(det['name'])
        else:
            break

def spacenet():
    list = spacenet_links()
    for l in list:
        spacenet_scraping_core(l['link'], l['info'])