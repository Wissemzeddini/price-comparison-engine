import requests
from bs4 import BeautifulSoup
import mysql.connector
from Apps.sqlQuery import *

def bestbuy_links():
    list=[]
    web = requests.get('https://bestbuytunisie.com/')
    parse = BeautifulSoup(web.content, 'html.parser')
    menu= parse.find('ul', id='menu-all-departments-menu-1').find_all('a')
    for m in menu:
        info= m.text
        link=m.get('href')
        if link != '#':
            bestbuy_dict={
                'info':info,
                'link':link
              }
            list.append(bestbuy_dict)
    return list

#extract single page details
def bestbuy_det(url):
    text = requests.get(url).text
    soup = BeautifulSoup(text, 'lxml')
    try:
        name= soup.find('h1', class_ ='product_title entry-title').text
    except:
        name = 'Unknown'
    try:
        brand = soup.find('table', class_='woocommerce-product-attributes shop_attributes').tr.td.text.replace(u'\n','')
    except:
        brand = 'Unknown'
    try:    
        des = soup.find('div', class_ = 'woocommerce-product-details__short-description').p.text.replace('–','').strip()
    except:
        des='None'
    label,data,list='','',[]
    try:
        table= soup.find('table', class_='woocommerce-product-attributes shop_attributes').find_all('tr')
        for t in table:
            label=t.th.text.strip()
            data=t.td.text.strip()
            dict={
                'label':label,
                'data':data
            }
            list.append(dict)
    except:
        list=[]
    article ={
          'name':name,
          'brand': brand,
          'des': des,
          'fich_tech':list
      }
    return article

def priceConv(price):
    c=''
    for p in price:
        if(p.isdigit()):
            c=c+p
    return int(c)

def next_url(url, x):
    if(x == 1):
        url=url+'page/'+str(x)
    else:
        url=url[:-1]
        if(x>10):
            url=url[:-1]
        url=url+str(x)
    web = requests.get(url)
    parse = BeautifulSoup(web.content, 'html.parser')
    if(parse.find('div', class_='info-404')):
        return False, parse  
  
    return url, parse

#bestbuy main scraping process
def bestbuy_scraping_core(link, info):
#     categorieAdd(info, link, 25)
#     supCatId=getCagId(info,25)
    for x in range(1,30):
        link, parse= next_url(link,x)
        print(link)
        if(not(link == False)):
            card= parse.find('ul', class_='products columns-4 columns__wide--5').find_all('li')
            for c in card:
                try:
                    stock= c.find('span', class_='wapl-label-text').text
                except:
                    stock= 'non disponible'
                try:
                    img= c.find('img', class_='attachment-woocommerce_thumbnail')['data-lazy-src']
                except:
                    img='None'
                try:
                    price= c.find('span', class_ ='price').text.replace(u'\xa0','')
                    price=priceConv(price)
                except:
                    price=0
                try:
                    det_link= c.find('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link')['href']
                    det=bestbuy_det(det_link)
                except:
                    det_link='None'
#                 brandAdd(det['brand'], 'None', 25)
#                 supBrandId=getBrandId(det['brand'], 25)
#                 prodId=AddProduct(det['name'], det_link, 'None', det['des'], price, stock, 25, supBrandId, supCatId, img)
#                 if(det['fich_tech']):
#                     AddProductAttribut(det['fich_tech'], prodId)
                print(det['name'])
        else:
            break

def bestbuy():
    list = bestbuy_links()
    for l in list:
        bestbuy_scraping_core(l['link'], l['info'])