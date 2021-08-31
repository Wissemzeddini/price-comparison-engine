import requests
from bs4 import BeautifulSoup
import mysql.connector
from Apps.sqlQuery import *

def sbs_links():
    sbs_list=[]
    web = requests.get('https://www.sbsinformatique.com/')
    parse = BeautifulSoup(web.content, 'html.parser')
    sbs_links= parse.find_all('a', class_="fontcustom2")
    for sbs in sbs_links:
        link=sbs['href']
        info=sbs.span.text
        if(not(info == 'PC BUILDER')):
          sbs_dict={
          'name':info,
          'link':link
          }
          sbs_list.append(sbs_dict)
    return sbs_list

def sbs_details(link):
    web = requests.get(link)
    parse = BeautifulSoup(web.content, 'html.parser')
    try:
        uid= parse.find('p', class_='reference').text
    except:
        uid='Undfined'
    try:
        stock= parse.find('span', id='product-availability').text.replace('\ue5ca','').strip()
    except:
        stock='non disonible'
    try:
        brand = parse.find('section', class_='page-content').img['src']
    except:
        brand='Unknown'
    try:
        des = parse.find('div', class_='product-desc').p.text
    except:
        des='None'
    label, data='',''
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
        fich_list[i]['data']=v.text
        i +=1
    details={
      'uid':uid,
      'stock':stock,
      'brand':brand,
      'des':des,
      'fich_tech':fich_list
    }
    return details

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

def sbs_info_scrap_core(link, info):
    #categorieAdd(info, link, 19)
    #supCatId=getCagId(info,19)
    for x in range(1,30):
        link, parse = next_url(link,x)
        if(not(link == False)):
            card= parse.find_all('div', class_='item-product col-xs-12 col-sm-6 col-md-6 col-lg-4')
            for c in card:
                name= c.find('a', class_='product_name').text
                img= c.find('a', class_='thumbnail product-thumbnail').img['src']
                price= c.find('div', class_='product-price-and-shipping').span.text.replace('&nbsp;','')
                det_link= c.find('a', class_='product_name')['href']
                det=sbs_details(det_link)
                #brandAdd(det['brand'], det['brand'], 19)
                #supBrandId=getBrandId(det['brand'], 19)
                #prodId=AddProduct(name, det_link, det['uid'], det['des'], price, det['stock'], 19, supBrandId, supCatId, img)
                if(det['fich_tech']):
                    #AddProductAttribut(det['fich_tech'], prodId)
                    pass
                print(name)
        else:
            break

def sbs_info():
    list = sbs_links()
    for l in list:
         sbs_info_scrap_core(l['link'], l['name'])
