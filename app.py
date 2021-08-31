from flask import Flask, render_template, url_for   
import mysql.connector
from Apps.main_scraping import *
from Apps.matching import main_matching_proccess
from Apps.model import predict_match

app = Flask(__name__) 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="scraping_data"
)
def supp_img(sup_id):
    id_=int(sup_id)
    if(id_==16):
        return "https://mk-static.mytek.tn/static/version1617227958/frontend/Sm/topmart/fr_FR/images/logo.svg"
    elif(id_==17):
        return "https://www.tunisianet.com.tn/img/tunisianet-logo-1611064619.jpg"
    elif(id_==18):
        return "https://www.wiki.tn/img/logo.jpg"
    elif(id_==19):
        return "https://www.sbsinformatique.com/img/prestashop-logo-1585766163.jpg"
    elif(id_==20):
        return "https://www.itechstore.tn/img/itech-store-logo-1545673222.jpg"
    elif(id_==21):
        return "https://www.scoop.com.tn/img/sp-g3shop-logo-1591977520.jpg"
    elif(id_==22):
        return "https://www.zoom.com.tn/img/zoom-informatique-logo-1503561020.jpg"
    elif(id_==23):
        return "https://spacenet.tn/img/spacenet-b2c-logo-1602842200.jpg"
    elif(id_==24):
        return "https://www.alarabia.com.tn/img/alarabia-informatique-logo-1614964355.jpg"
    else:
        return "https://bestbuytunisie.com/wp-content/uploads/2021/02/cropped-logo-best-buy-Tunisie.png"

def refrenced_store(nb):
    if(nb == 16):
        return "Mytek"
    elif(nb == 17):
        return "Tunisianet"
    elif(nb == 18):
        return "wiki"
    elif(nb == 19):
        return "sbsinformatique"
    elif(nb == 20):
        return "itechstore"
    elif(nb == 21):
        return "Scoop"
    elif(nb == 22):
        return "Zoom"
    elif(nb == 23):
        return "Spacenet"
    elif(nb == 24):
        return "Alarabia"
    else:
        return "BestBuy"

def refrenced_catg(uid):
    mycursor = mydb.cursor()
    query="""SELECT name FROM supplier_categories WHERE id = %s"""
    val=(uid,)
    mycursor.execute(query,val)
    res = mycursor.fetchone()
    return res

def getListSimilar(prod_id):
    mycursor = mydb.cursor()
    query="""SELECT s.id, s.name,s.img,s.price,s.supplier_id FROM matching m, supplier_products s WHERE m.prod_id_two = s.id and m.prod_id_one = %s and m.class=1"""
    val =(prod_id,)
    mycursor.execute(query,val)
    results = mycursor.fetchall()
    list=[]
    for res in results:
        img=supp_img(res[4])
        dict={
        'id':res[0],
        'name':res[1],
        'img': res[2],
        'price':res[3],
        'sup_img':img
        }
        list.append(dict)
    return list

def getDataCategory(uid):
    mycursor = mydb.cursor()
    query="""SELECT DISTINCT s.id, s.name, s.description, s.availability,s.img,s.price FROM matching m, supplier_products s WHERE m.prod_id_one = s.id and supplier_category_id = %s"""
    val=(uid,)
    mycursor.execute(query,val)
    results = mycursor.fetchall()
    return results
 
def store_stat():
    mycursor = mydb.cursor()
    list=[]
    for i in range(16,26):
        query="""SELECT count(*) FROM supplier_products WHERE supplier_id = %s"""
        val=(i,)
        mycursor.execute(query,val)
        res = mycursor.fetchone()[0]
        dict={
            'Store': refrenced_store(i),
            'nb_prod': int((res/19159)*100)
        }
        list.append(dict)
    return list

def category_stat():
    list=[]
    mycursor = mydb.cursor()
    for i in range(26,65):
        query=""" SELECT count(*) FROM supplier_products WHERE supplier_category_id = %s"""
        val=(i,)
        mycursor.execute(query,val)
        res = mycursor.fetchone()[0]
        dict={
            'catg_id': refrenced_catg(i),
            'pd_count': int((res/8371)*100)
        }
        list.append(dict)
    list.sort(key=lambda l: l['pd_count'], reverse=True)
    return list

@app.route("/")                   
def index():     
    uid=26
    res = getDataCategory(uid)
    return render_template('index.html', data=res)

@app.route("/category/<int:uid>")                   
def show_cag(uid):     
    res = getDataCategory(uid)
    return render_template('index.html', data=res)

@app.route("/single/<int:prod_id>")
def single(prod_id):

     mycursor = mydb.cursor()
     query = """ SELECT * from supplier_products where id = %s"""
     val = (prod_id,)
     mycursor.execute(query,val)
     res = mycursor.fetchone()
     query = """SELECT * FROM suppliers where id = %s"""
     val = (res[8],)
     mycursor.execute(query,val)
     r = mycursor.fetchone()
     query = """SELECT * FROM supplier_brands where id = %s"""
     val = (res[9],)
     mycursor.execute(query,val)
     re = mycursor.fetchone()
     list=getListSimilar(prod_id)
     return render_template("single.html", res=res,logo=r[4],brand=re[1], list=list)

@app.route("/admin")
def dashboard():
    list = store_stat()
    list2 = category_stat()
    return render_template("admin.html", data=list, catg=list2)

@app.route("/scraping")
def scraping():
    scraping_main_process()

@app.route("/matching")
def matching():
    main_matching_proccess()

@app.route("/model")
def modeling():
    predict_match()
    list = store_stat()
    list2 = category_stat()
    return render_template("admin.html", data=list, catg=list2)

if __name__ == "__main__":        
    app.run()       