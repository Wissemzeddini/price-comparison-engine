import requests
from bs4 import BeautifulSoup
import mysql.connector
from Apps.sqlQuery import *

scoop_list=[{
    'info': 'Ordinateurs & Tablettes',
    'link': 'https://www.scoop.com.tn/320-ordinateurs-tablettes'
},{
    'info':'Ecrans',
    'link':'https://www.scoop.com.tn/292-ecrans',
},{
    'info':'Serveurs & Stockage',
    'link':'https://www.scoop.com.tn/299-serveurs-et-stockage'
},{
    'info':'Imprimantes & copieurs',
    'link':'https://www.scoop.com.tn/294-imprimantes'
},
{
    'info':'Photos & Vidéoprojecteurs',
    'link':'https://www.scoop.com.tn/2069-photo-videoprojecteurs'
},{
    'info':'Réseau & connectique',
    'link':'https://www.scoop.com.tn/2064-reseau-connectique'
},
{
    'info':'Logiciels',
    'link':'https://www.scoop.com.tn/142-logiciels'
},{
    'info':'Accessoires Informatique',
    'link':'https://www.scoop.com.tn/293-accessoires-informatique'
},{
    'info':'Consoles et jeux',
    'link':'https://www.scoop.com.tn/2068-consoles-et-jeux'
}]

def getThatPart(ch):
    i,j=0,0
    for x in range(2, len(ch)):
        if(ch[x] == '>'):
            i = x
        elif(ch[x] == '<'):
            j = x
            break
    return ch[i+1:j]

def priceConv(price):
    c=''
    for p in price:
        if(p.isdigit()):
            c=c+p
    return int(c)

def scoop_details(link):    
    web = requests.get(link)
    parse = BeautifulSoup(web.content, 'html.parser')
    try:
        name= parse.find('div', class_='product-info').h1.text
    except:
        name='Unknown'
    try:
        uid= parse.find('div', id='short_description_block').span.text.replace('Référence : ','')
    except:
        uid='Undifined'
    try:
        price= parse.find('span', id='our_price_display').text
        price = priceConv(price)
    except:
        price=0
    try:
        brand_logo = parse.find('div', id='short_description_content').p.img['src']
    except:
        brand_logo='Unknown'
    try:
        des = parse.find('div', id='short_description_content').text
    except:
        des='None'
    boutique, etat='',''
    list=[]
    try:
        localstore= parse.find_all('div', class_='block_dispo_magazin')
        for l in localstore:
            boutique = str(l.a)
            etat= l.a.span.text
            dict={
                'magasin':getThatPart(boutique),
                'status':etat
            }
            list.append(dict)
    except:
        list=[]
    list_tech=[]
    title, feautre='',''
    try:
        fich_tech= parse.find('table', class_='table-data-sheet').find_all('tr')
        for f in fich_tech:
            title=f.td.text
            feautre= [t.text for t in f.find_all('td')][1]
            fich_dec={
                'label':title,
                'data':feautre
            }
            list_tech.append(fich_dec)
    except:
        list_tech=[]
    details={
          'name':name,
          'uid':uid,
          'price':price,
          'brand_logo':brand_logo,
          'des':des,
          'localstore':list,
          'list_tech':list_tech
      }
    return details

# mycursor = mydb.cursor()
for l in scoop_list:
    info=l['info']
    link=l['link']
    categorieAdd(info, link, 21)
    supCatId=getCagId(info,21)
    web = requests.get(link)
    parse = BeautifulSoup(web.content, 'html.parser')
    card= parse.find_all('li', class_='ajax_block_product')
    for c in card:
        det_link =c.find('h5', class_='product-name').a['href']
        try:
            img=c.find('div',class_='product-image').a.img['src']
        except:
            img='None'
        try:
            stock= c.find('span', class_='available-now').text
        except:
            stock= 'Undfined'
        det= scoop_details(det_link)
        brandAdd(det['brand_logo'], det['brand_logo'], 21)
        supBrandId=getBrandId(det['brand_logo'],21)
        prodId=AddProduct(det['name'], det_link, det['uid'], det['des'], det['price'], stock, 21, supBrandId, supCatId, img)
        if(det['localstore']):
            Addlocalstors(det['localstore'], 21)
            AddLocalStoreProduct(det['localstore'], det['price'], prodId, 21)
        if(det['list_tech']):
            AddProductAttribut(det['list_tech'], prodId)