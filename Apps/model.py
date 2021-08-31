import pickle
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="scraping_data"
)

mycursor = mydb.cursor()
model = pickle.load(open('Apps/finalized_model.sav', 'rb'))

def loadMatch():
    list=[]
    query="SELECT * FROM matching where class=0"
    mycursor.execute(query)
    results = mycursor.fetchall()
    for res in results:
        dict={
            'id':res[0],
            'name_score':res[3],
            'name_number_rate':res[4],
            'des_score':res[5],
            'img_score':res[6],
            'att_score':res[7],
            'score':res[8]
        }
        list.append(dict)
    return list

def update(m_id, match):
    query="UPDATE matching SET class = %s WHERE id = %s"
    val=(match,m_id,)
    mycursor.execute(query,val)
    mydb.commit()

def predict_match():
    for l in loadMatch():
        name_score=int(l['name_score'])
        name_number_rate=int(l['name_number_rate'])
        des_score=int(l['des_score'])
        img_score=int(l['img_score'])
        att_score=int(l['att_score'])
        res=model.predict([[name_score,name_number_rate,des_score,img_score,att_score]])
        #update(int(l['id']), int(res[0]))
        print(l['id'], end=" ")