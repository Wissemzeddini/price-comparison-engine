import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="scraping_data"
)

def create_suppliers():
    mycursor = mydb.cursor()
    now = datetime.now()
    suppliers_list=[{'name':'Mytek', 'code':'None', 'uri':'https://www.mytek.tn/','logo_link':'https://mk-static.mytek.tn/static/version1617227958/frontend/Sm/topmart/fr_FR/images/logo.svg'},
                    {'name':'Tunisianet','code':'None','uri':'https://www.tunisianet.com.tn/','logo_link':'https://www.tunisianet.com.tn/img/tunisianet-logo-1611064619.jpg'},
                    {'name':'Wiki','code':'None','uri':'https://www.wiki.tn/','logo_link':'https://www.wiki.tn/img/logo.jpg'},
                    {'name':'SBS Informatique','code':'None','uri':'https://www.sbsinformatique.com/accueil/pc-sur-mesure-tunisie.html','logo_link':'https://www.sbsinformatique.com/img/prestashop-logo-1585766163.jpg'},
                    {'name':'iTech Store','code':'None','uri':'https://www.itechstore.tn/','logo_link':'https://www.itechstore.tn/img/itech-store-logo-1545673222.jpg'},
                    {'name':'Scoop','code':'None','uri':'https://www.scoop.com.tn/','logo_link':'https://www.scoop.com.tn/img/sp-g3shop-logo-1591977520.jpg'},
                    {'name':'Zoom','code':'None','uri':'https://www.zoom.com.tn/','logo_link':'https://www.zoom.com.tn/img/zoom-informatique-logo-1503561020.jpg'},
                    {'name':'Space Net','code':'None','uri':'https://spacenet.tn/','logo_link':'https://spacenet.tn/img/spacenet-b2c-logo-1602842200.jpg'},
                    {'name':'Alarabia','code':'None','uri':'https://www.alarabia.com.tn/','logo_link':'https://www.alarabia.com.tn/img/alarabia-informatique-logo-1614964355.jpg'},
                    {'name':'Best Buy','code':'None','uri':'https://bestbuytunisie.com/','logo_link':'https://bestbuytunisie.com/wp-content/uploads/2021/02/cropped-logo-best-buy-Tunisie.png'}]
    for l in suppliers_list:
        sql = "INSERT INTO suppliers (name, code, uri, logo_link, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (l['name'], l['code'], l['uri'], l['logo_link'], now, now)
        mycursor.execute(sql, val)
        mydb.commit()
    mycursor.close()

def brandAdd(name, logo, supId):
    mycursor = mydb.cursor()
    now = datetime.now()
    query="""SELECT * FROM supplier_brands where name=%s and supplier_id=%s"""
    value=(name, supId)
    mycursor.execute(query, value)
    results = mycursor.fetchall()
    if(mycursor.rowcount == 0):
        sql = "INSERT INTO supplier_brands (name, logo_location, supplier_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)"
        val = (name, logo, supId, now, now)
        mycursor.execute(sql, val)
        mydb.commit()
        #print('ok')
    mycursor.close()

def getBrandId(name, supId):
    brandId=0
    mycursor = mydb.cursor()
    query="""SELECT * FROM supplier_brands where name=%s and supplier_id=%s"""
    value=(name, supId)
    mycursor.execute(query, value)
    results = mycursor.fetchall()
    for res in results:
        brandId=res[0]
    return brandId

def categorieAdd(name, uri, supId):
    mycursor = mydb.cursor()
    now = datetime.now()
    sql = "INSERT INTO supplier_categories (name, uri, supplier_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)"
    val = (name, uri, supId, now, now)
    try:
        mycursor.execute(sql, val)
        mydb.commit()
        #print('ok')
    except:
        print('Data Base Categorie Duplication Error\n')
    mycursor.close()

def  getCagId(categ,supId):
    cagId=0
    mycursor = mydb.cursor()
    query="""SELECT * FROM supplier_categories where name=%s and supplier_id=%s"""
    value=(categ, supId)
    mycursor.execute(query, value)
    results = mycursor.fetchall()
    for res in results:
        cagId=res[0]
    mycursor.close()
    return cagId

def AddProduct(name, uri, sku, des, price, availability, supId, supBrandId, supCatId, img):
    mycursor = mydb.cursor()
    now = datetime.now()
    productId=0
    sql = "INSERT INTO supplier_products (name, uri, sku, description, price, availability, supplier_id, supplier_brand_id, supplier_category_id, created_at, updated_at, img) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (name, uri, sku, des, price, availability, supId, supBrandId, supCatId, now, now ,img)
    try:
        mycursor.execute(sql, val)
        mydb.commit()
    except:
        print('Product Duplicate Error')
    query="""SELECT * FROM supplier_products where name=%s and sku=%s and supplier_id=%s"""
    value=(name, sku, supId)
    mycursor.execute(query, value)
    results = mycursor.fetchall()
    for res in results:
        productId=res[0]
    mycursor.close()
    return productId

def Addlocalstors(localstore, supId):
    mycursor = mydb.cursor()
    now = datetime.now()
    if(localstore):
        for l in localstore:
            query="""SELECT * FROM localstores where name=%s and supplier_id=%s"""
            value=(l['magasin'], supId)
            mycursor.execute(query, value)
            results = mycursor.fetchall()
            #print(mycursor.rowcount)
            if(mycursor.rowcount == 0):
                sql = "INSERT INTO localstores (name, supplier_id, created_at, updated_at) VALUES (%s, %s, %s, %s)"
                val = (l['magasin'], supId, now, now)
                mycursor.execute(sql, val)
                mydb.commit()
                #print(ok)
    mycursor.close()

def getLocalstoreId(magasin, supId):
    localstoreId=False
    mycursor = mydb.cursor()
    query="""SELECT * FROM localstores where name=%s and supplier_id=%s"""
    value=(magasin, supId)
    mycursor.execute(query, value)
    results = mycursor.fetchall()
    if(mycursor.rowcount > 0):
        for res in results:
            localstoreId=res[0]
    mycursor.close()
    return localstoreId

def AddLocalStoreProduct(localstore, price, prodId, supId):
    mycursor = mydb.cursor()
    now = datetime.now()
    localstoreId=0
    if(localstore):
        for l in localstore:
            localstoreId=getLocalstoreId(l['magasin'], supId)
            sql = "INSERT INTO localstore_products (price, availability, localstore_id, supplier_product_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (price, l['status'], localstoreId, prodId, now, now)
            try:
                mycursor.execute(sql, val)
                mydb.commit()
                #print('ok')
            except:
                print('localstore product Add fails')
    mycursor.close()

def AddProductAttribut(fich_tech, prodId):
    mycursor = mydb.cursor()
    now = datetime.now()
    if(fich_tech):
        for f in fich_tech:
            sql = "INSERT INTO supplier_product_attributes (name, value, supplier_product_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)"
            val = (f['label'], f['data'], prodId, now, now)
            try:
                mycursor.execute(sql, val)
                mydb.commit()
                #print('ok')
            except:
                print('Add Product Attribut Fails')
    mycursor.close()  