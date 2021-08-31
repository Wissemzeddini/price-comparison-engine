import requests
from bs4 import BeautifulSoup
import mysql.connector
from Apps.sqlQuery import *

def wikiGetLinks():
    list=[]
    web = requests.get('https://www.wiki.tn/')
    parse = BeautifulSoup(web.content, 'html.parser')
    catalogue= parse.find_all('li', class_='parent dropdown-submenu')
    for cag in catalogue:
        link=cag.a['href'].replace('é','e')
        info=cag.a.span.text.strip()
        dect={
            'info':info,
            'link':link
            }
        list.append(dect)
    return list

#exract wiki data from details page
def wiki_details(url):
    list=[]
    web = requests.get(url)
    parse = BeautifulSoup(web.content, 'html.parser')
    try:
        brand_logo= parse.find('span', class_='marque').img['src']
    except:
        brand_logo=''
    try:
        sku=parse.find('p', id='product_reference').span.text.strip()
    except:
        sku='undfined'     
    try:
        des= parse.find('div', id='short_description_block').text.strip()
    except:
        des='None'
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
    article={
        'sku':sku,
        'brand_logo':brand_logo,
        'des':des,
        'fiche_technique':list
    }
    return article

def next_url(link, x):
    if(x==1):
        link =link+'#/page-'+str(x)
    else:
        link=link[:-1]
        if(x>10):
            link=link[:-1]
        link=link+str(x)
    text = requests.get(link)
    parse = BeautifulSoup(text.content, 'html.parser')
    try:
        nb= parse.find('div',class_='product-count pull-right').text
    except:
        nb='Résultats 1 - 12 sur 5 produits'
    return link, parse, getTotalProduits(nb)   

#convert string price to integer
def priceConv(price):
    c=''
    for p in price:
        if(p.isdigit()):
            c=c+p
    return int(c)

def wiki_scraping_core(link, info):
    #categorieAdd(info, link, 18)
    #supCatId=getCagId(info,18)
    i=0
    for x in range(1,30):
        link, parse, nb = next_url(link, x)
        print(link)
        if(i < nb):
            art= parse.find_all('div', class_='product-container product-block')
            for a in art:
                i=i+1
                name= a.find('a', class_='product-name').text
                try:
                    price = a.find('span', class_='price product-price').text
                    price = priceConv(price)
                except:
                    price=0
                art_link=a.find('a', class_='product-name').get('href')
                try:
                    brand= a.find('div', class_='logo_marque').img['alt']
                except:
                    brand='Unkown'
                img = a.find('a', class_='product_img_link').img['src']
                stock= a.find('span', class_='availability').span.text
                det= wiki_details(art_link)
                #brandAdd(brand, det['brand_logo'], 18)
                #supBrandId=getBrandId(brand, 18)
                #prodId=AddProduct(name, art_link, det['sku'], det['des'], price, stock, 18, supBrandId, supCatId, img)
                if(det['fiche_technique']):
                    #AddProductAttribut(det['fiche_technique'], prodId)
                    pass
                print(name)
        else:
            break
        
def wiki():
    list = wikiGetLinks()
    for l in list:
        wiki_scraping_core(l['link'], l['info'])

   