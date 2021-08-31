import requests
from bs4 import BeautifulSoup
import mysql.connector
#import ipynb
from Apps.sqlQuery import *

def mytek_links():   
    list=[]
    web = requests.get('https://www.mytek.tn/')
    parse = BeautifulSoup(web.content, 'html.parser')
    card = parse.find_all('div', class_ = 'sm_megamenu_head_item')
    for c in card:
        name = c.find('a', class_='sm_megamenu_nodrop').text.strip()
        link = c.find('a', class_='sm_megamenu_nodrop')['href']
        if(name != 'Voir +'):
            dict={
                'name': name,
                'link': link
            }
            list.append(dict)
    return list

def mytek_det(url):
    text = requests.get(url).text
    soup = BeautifulSoup(text, 'lxml')
    try:
        name= soup.find('h1', class_ ='page-title').span.text
    except:
        name = 'Unknown'
    try:
        brand = soup.find('div', class_='amshopby-option-link').a['title'].replace(' ','').strip()
    except:
        brand = 'Unknown'
    try:
        brand_logo = soup.find('div', class_='amshopby-option-link').img['src']
    except:
        brand_logo ='None'
    try:
        price= soup.find('span', class_ ='price-container price-final_price tax weee').span.span.text.replace('&nbsp;','')
    except:
        price = '0TND'
    try:
        stock = soup.find('div', class_ = 'product-info-stock-sku').div.span.text.strip()
    except:
        stock = 'épuise'
    try:
        sku = soup.find('div', class_ = 'value').text.strip()
    except:
        sku = 'None'
    try:    
        des = soup.find('div', class_ = 'product attribute overview').div.p.text.strip()
    except:
        des='None'

    magsin_list=[]
    fiche_tech=[]
    magasin, status= '',''
    try:
        local_store = soup.find('table', class_='tab_retrait_mag').find_all('tr')
        for l in local_store:
                text=l.text.split(':')
                if(len(text)>1):
                    mag_dict={
                            'magasin':text[0],
                            'status':text[1]
                            }
                    magsin_list.append(mag_dict)
    except:
        magsin_list='None'
    try:
        fiche_technique= soup.find('table', class_='data table additional-attributes').find_all('tr')
        for f in fiche_technique:
                column1= f.find('th').text
                column2= f.find('td').text
                fiche_dict={
                   'label':column1,
                    'data':column2
                }
                fiche_tech.append(fiche_dict)
    except:
        fiche_tech=[]
    article ={
            'name':name,
            'brand': brand,
            'brand_logo':brand_logo,
            'price': price,
            'stock': stock,
            'sku': sku,
            'des': des,
            'local_store':magsin_list,
            'fiche_tech':fiche_tech
        }
    return article

def next_url(url, x):
    if(x == 1):
        url=url+'?p='+str(x)
    else:
        url=url[:-1]
        if(x>10):
            url=url[:-1]
        url=url+str(x)
    web = requests.get(url)
    parse = BeautifulSoup(web.content, 'html.parser')
    if(parse.find('div', class_='message info empty')):
        return False, parse 
    
    return url, parse

def mytek_scraping_core(link, info):
    #categorieAdd(info, link, 16)
    #supCatId=getCagId(info,16)
    for x in range(1,53):
        link, soup = next_url(link,x)
        if(not(link == False)):
            prod = soup.find_all('li', class_ = 'item product product-item')
            for p in prod:
                url = p.find('a', class_ = 'product photo product-item-photo')['href']
                try:
                    img=p.find('div',class_='image-product').a.span.span.img.get('src')
                except:
                    img='None'
                try:
                    det= mytek_det(url)
                    #brandAdd(det['brand'], det['brand_logo'], 16)
                    #supBrandId=getBrandId(det['brand'],16)
                    #prodId=AddProduct(det['name'], url, det['sku'], det['des'], det['price'], det['stock'], 16, supBrandId, supCatId, img)
                    if(det['local_store'] != 'None'):
                        #Addlocalstors(det['local_store'], 16)
                        #AddLocalStoreProduct(det['local_store'], det['price'], prodId, 16)
                        pass
                    if(det['fiche_tech']):
                        pass
                        #AddProductAttribut(det['fiche_tech'], prodId)
                    print(det['name'])
                except:
                    pass
        else:
            break
                       
def mytek():
    list = mytek_links()
    for l in list:
        mytek_scraping_core(l['link'], l['name'])  
