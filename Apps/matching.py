#import python library 
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import mysql.connector
import re
import cv2
from PIL import Image
import requests
import numpy as np
import math

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="scraping_data"
)
mycursor = mydb.cursor()

def get_rate(product1, product2):    
    regex = r'[0-9]+'
    numbers1 = set(re.findall(regex, product1))
    numbers2 = set(re.findall(regex, product2))
    union = numbers1.union(numbers2)
    intersection = numbers1.intersection(numbers2)
    if len(numbers1)==0 and len(numbers2) == 0:
        rate = 0
    else:
        rate = (len(intersection)/ len(union))
    return int(rate*100)

def loadDataM(supid):
    list=[]
    query="SELECT * FROM supplier_products where supplier_id = %s and id>1142"
    val=(supid,)
    try:
        mycursor.execute(query, val)
        results = mycursor.fetchall()
        for res in results:
            dict={
                'id':res[0],
                'name':res[1],
                'catgory':res[10],
                'des':res[5],
                'brand_id':res[9],
                'img':res[13]
            }
            list.append(dict)
    except:
         list=[]
    return list

# load Mysql table supplier_product data with filter by supplier id
def loadData(supid):
    list=[]
    query="SELECT * FROM supplier_products where supplier_id = %s"
    val=(supid,)
    try:
        mycursor.execute(query, val)
        results = mycursor.fetchall()
        for res in results:
            dict={
                'id':res[0],
                'name':res[1],
                'catgory':res[10],
                'des':res[5],
                'brand_id':res[9],
                'img':res[13]
            }
            list.append(dict)
    except:
         list=[]
    return list

def loadMatch(id):
    list1=[]
    list2=[]
    list=[]
    query="SELECT * FROM matching where prod_id_one = %s"
    val=(id,)
    mycursor.execute(query, val)
    results = mycursor.fetchall()
    for res in results:
        dict1={
            'id1':res[1],
            'id2':res[2],
            'score':res[8]
        }
        list1.append(dict1)
    query="SELECT * FROM matching where prod_id_two = %s"
    val=(id,)
    mycursor.execute(query, val)
    results = mycursor.fetchall()
    for res in results:
        dict2={
            'id1':res[2],
            'id2':res[1],
            'score':res[8]
        }
        list2.append(dict1)     
    list=list1+list2
    return list

def in_group_exist_verify(id1,id2):
    list1=loadMatch(id1)
    list2=loadMatch(id2)
    for l1 in list1:
        for l2 in list2:
            if(l1['id'] == l2['id'] > 85):
                return False
    return True

def getCatgory(uid):
    query="SELECT * FROM supplier_categories where id = %s"
    val=(uid,)
    try:
        mycursor.execute(query, val)
        result = mycursor.fetchone()[1]
    except:
         result=None
    return str(result)

def getBrand(uid):
    query="SELECT * FROM supplier_brands where id = %s"
    val=(uid,)
    try:
        mycursor.execute(query, val)
        result = mycursor.fetchone()[1]
    except:
         result=None
    return str(result)

def similar(ch1,ch2):
    result = fuzz.partial_ratio(ch1.lower(), ch2.lower())
    if result > 75:
        return True
    else:
        return False

def getAttr(id):
    string=''
    query="SELECT * FROM supplier_product_attributes where supplier_product_id=%s"
    val=(id,)
    mycursor.execute(query, val)
    results = mycursor.fetchall()
    #print(len(results))
    for res in results:
        string=string + res[1]+' '+res[2]+' '
    return string

def AttributeScore(prod1,prod2):
    ch1=getAttr(prod1)
    ch2=getAttr(prod2)
    if(ch1 == '' or ch2 == ''):
        return 1
    return  fuzz.partial_ratio(ch1.lower(), ch2.lower())

def imageSimilarty(url, url1):
    # image1
    try:
        img = Image.open(requests.get(url, stream=True).raw)
        gray_image = cv2.cvtColor(np.float32(img), cv2.COLOR_BGR2GRAY)
        histogram = cv2.calcHist([gray_image], [0], 
                                 None, [256], [0, 256])
    except:
        return 10
    # image2
    try: 
        img1 = Image.open(requests.get(url1, stream=True).raw)
        gray_image1 = cv2.cvtColor(np.float32(img1), cv2.COLOR_BGR2GRAY)
        histogram1 = cv2.calcHist([gray_image1], [0], 
                                  None, [256], [0, 256])
    except:
        return 10
    c1, c2 = 0, 0

    # Euclidean Distace between data1 and test
    i = 0
    while i<len(histogram) and i<len(histogram1):
        c1+=(histogram[i]-histogram1[i])**2
        i+= 1
    c1 = c1**(1 / 2)
    c=c1[0]
    return math.floor(100-(c/1000))

def brandVerify(brand1, brand2):
    result = fuzz.partial_ratio(brand1, brand2)
    if(brand1 == 'Unknown' or brand2 == 'Unknown'):
        return True
    elif(brand1.startswith("https") or brand2.startswith("https")):
        return True
    elif(brand1.startswith("..") or brand2.startswith("..")):
        return True
    elif(result > 80):
        return True
    else:
        return False 

def saveMatching(id1,id2,nameScore,nameNumberRate,brandScore,imgScore,attrScore,score):
    if(score > 60):
        query="INSERT INTO matching (prod_id_one, prod_id_two, name_score, name_number_rate, des_score, image_score, attr_score, score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val=(id1, id2, nameScore, nameNumberRate, desScore, imgScore, attrScore, score)
        mycursor.execute(query, val)
        mydb.commit()

def average_correction(nscore,nnrate,dscore,imscore,atscore):
    divided_by=19
    if(atscore == 1 or atscore == 0):
        atscore = 0
    else:
        divided_by =  divided_by + 3
        atscore =  atscore*3
    if(imscore > 10):
        divided_by=divided_by + 1
    else:
        imscore = 0
    
    #print("average repport:",divided_by," att score: ",atscore," imscore: ",imscore)
    return ((nscore*10) + (nnrate*3) +(dscore*6) + (imscore) + (atscore))//divided_by

# main algorithm matching process
def main_matching_proccess():
	list1 = loadDataM(16)
	for l1 in list1:
	    for x in range(17,26):
	        list2= loadData(x)
	        print("-------------->",l1['id'])
	        for l2 in list2:
	            if(similar(getCatgory(l1['catgory']), getCatgory(l2['catgory'])) and brandVerify(str(getBrand(l1['brand_id'])).lower(), str(getBrand(l2['brand_id'])).lower())):
	                nameScore= fuzz.partial_ratio(l1['name'].lower(), l2['name'].lower())
	                desScore= fuzz.partial_ratio(str(l1['des']).lower(), str(l2['des']).lower())
	                nameNumberRate=get_rate(str(l1['name']),str(l2['name']))
	                #brandScore=fuzz.partial_ratio(str(getBrand(l1['brand_id'])).lower(), str(getBrand(l2['brand_id'])).lower())
	                imgScore = imageSimilarty(str(l1['img']), str(l2['img']))
	                attrScore=AttributeScore(str(l1['id']),str(l2['id']))
	                moy=average_correction(nameScore,nameNumberRate,desScore,imgScore,attrScore)
	                print(f'{nameScore}-->{nameNumberRate}-->{desScore}-->{imgScore}-->{attrScore}-->{moy}')
	                #saveMatching(l1['id'],l2['id'],nameScore,nameNumberRate,desScore,imgScore,attrScore,moy)