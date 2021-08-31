import requests
from bs4 import BeautifulSoup
import mysql.connector
from Apps.sqlQuery import *

def zoom_links():
    zoom_list=[]
    web = requests.get('https://www.zoom.com.tn/').text
    parse = BeautifulSoup(web, 'lxml')
    head= parse.find_all('li', class_='parent')
    for h in head:
        try:
            link= h.find('a', class_='dropdown-toggle has-category').get('href')
            info= h.find('a', class_='dropdown-toggle has-category').text
        except:
            link = 'None'
            info ='None'
        if link != 'None':
            zoom_dict={
                'link': link,
                'info': info
            }
            zoom_list.append(zoom_dict)
    return zoom_list

def priceConv(price):
    c=''
    for p in price:
        if(p.isdigit()):
            c=c+p
    return int(c)

def zoom_details(link):
    web = requests.get(link)
    parse = BeautifulSoup(web.content, 'html.parser')
    list=[]
    try:
        name= parse.find('div', class_='pb-right-column col-xs-12 col-sm-4 col-md-4').h1.text
    except:
        name= 'None'
    try:
        uid= parse.find('span', class_='editable').text
    except:
        uid='Undifined'
    try:
        brand = parse.find('div', class_='marque_name').a.img.get('alt')
        brand_logo = parse.find('div', class_='marque_name').a.img.get('src')
    except:
        brand='Unknown'
        brand_logo='Undfined'
    try:
        des = parse.find('div', class_ ='rte align_justify').text.strip()
    except:
        des= 'None'
    try:
        img = parse.find('span', id ='view_full_size').img['src']
    except:
        img='None'
    try:
        price = parse.find('span', id ='our_price_display').text
        price = priceConv(price)
    except:
        price='Undfined'
    title,feautre='',''
    try:
        fich_tech= parse.find('table', class_='table-data-sheet').find_all('tr')
        for f in fich_tech:
            title=f.td.text
            feautre= [t.text for t in f.find_all('td')][1]
            fich_dec={
                'label':title.strip(),
                'data':feautre.strip()
            }
            list.append(fich_dec)
    except:
        list=[]
    details={
        'name':name,
        'uid':uid,
        'brand':brand,
        'brand_logo':brand_logo,
        'des':des,
        'img':img,
        'price':price,
        'fich_tech':list
    }
    return details

def next_url(url, x):
    if(x == 1):
        url=url+'#/page-'+str(x)
    else:
        url=url[:-1]
        if(x>10):
            url=url[:-1]
        url=url+str(x)
    return url

def paginnation_lengh(info):
    if(info=='Informatique'):
        nb=4
    elif(info=='Téléphonie | Tablettes'):
        nb=4
    elif(info=='Stockage'):
        nb=2
    elif(info=='Impression | Scanner'):
        nb=2
    elif(info=='Photo & Vidéo'):
        nb=1
    elif(info=='Image & son'):
        nb=2
    elif(info=='Bureautique '):
        nb=4
    elif(info=='Electroménager'):
        nb=4
    elif(info=='Mode Beauté & Santé'):
        nb=1
    else:
        nb=1
        
    return nb

def zoom_scraping_core(link, info):
#     categorieAdd(info, link, 22)
#     supCatId=getCagId(info,22)
    leng=paginnation_lengh(info)
    for x in range(1,leng+1):
        link= next_url(link,x)
        print(link)
        web = requests.get(link)
        parse = BeautifulSoup(web.content, 'html.parser')
        card= parse.find_all('div', class_='ajax_block_product')
        for c in card:
            try:
                stock = c.find('span', class_='available-now').text
            except:
                stock='non disponible'
            try:
                det_link= c.find('a', class_='add_to_compare compare')['href']
            except:
                det_link='NO LINKS'
            if(det_link != 'NO LINKS'):
                det=zoom_details(det_link)
                print(det['name'])
#                 brandAdd(det['brand'], det['brand_logo'], 22)
#                 supBrandId=getBrandId(det['brand'], 22)
#                 prodId=AddProduct(det['name'], det_link, det['uid'], det['des'], det['price'], stock, 22, supBrandId, supCatId, det['img'])
#                 if(det['fich_tech']):
#                     AddProductAttribut(det['fich_tech'], prodId)        


def zoom():
    list = zoom_links()
    for l in list:
        zoom_scraping_core(l['link'], l['info'])