from flask import Flask,render_template,request
from flask_mysqldb import MySQL
import pandas as pd
import numpy as np
import jinja2
import pickle
app=Flask(__name__)
model=pickle.load(open('LinearRegressionModel.pkl','rb'))
car=pd.read_csv("Cleaned car.csv")
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= '123456'
app.config['MYSQL_DB']= 'flaskapp'

mysql=MySQL(app)
var_list=[]

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/result')
def result():
    companies=sorted(car['company'].unique())
    car_models=sorted(car['name'].unique())
    year=sorted(car['year'].unique(),reverse=True)
    fuel_type=car['fuel_type'].unique()
    return render_template('index2.html',companies=companies,car_models=car_models,years=year,fuel_types=fuel_type)

@app.route('/predict',methods=['POST'])
def predict():
    company=request.form.get('company')
    car_model=request.form.get('car_model')
    year=int(request.form.get('year'))
    fuel_type=request.form.get('fuel_type')
    kms_driven=int(request.form.get('kilo_driven'))
    var_list.append(company)
    var_list.append(car_model)
    var_list.append(year)
    var_list.append(fuel_type)
    var_list.append(kms_driven)
    print(company,car_model,year,fuel_type,kms_driven)
    prediction=model.predict(pd.DataFrame([[car_model,company,year,kms_driven,fuel_type]],columns=['name','company','year','kms_driven','fuel_type']))
    var_list.append(str(np.round(prediction[0],2)))
    if np.round(prediction[0],2)<0:
        return "Price is too low to sell"
    else:
        return "Prediction: ₹" + str(np.round(prediction[0],2))

@app.route('/sell',methods=['GET','POST'])
def sell():
    if request.method=='POST':
        userDetails= request.form
        name= userDetails['name']
        phone=userDetails['phone']
        address=userDetails['address']
        company=var_list.pop(0)
        car_model=var_list.pop(0)
        year=var_list.pop(0)
        fuel_type=var_list.pop(0)
        kilo_driven=var_list.pop(0)
        prediction=var_list.pop(0)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO sell(name,phone,address,company,car_model,year,fuel_type,kilo_driven,prediction) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name,phone,address,company,car_model,year,fuel_type,kilo_driven,prediction))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template("index2.html")

@app.route('/car1',methods=['GET','POST'])
def car1():
    if request.method=='POST':
        userDetails= request.form
        name= userDetails['name']
        phone=userDetails['phone']
        address=userDetails['address']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name,phone,address,car,value) VALUES(%s,%s,%s,%s,%s)",(name,phone,address,'BMW 7 series','₹1500k'))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template("car1.html")

@app.route('/car2',methods=['GET','POST'])
def car2():
    if request.method=='POST':
        userDetails= request.form
        name= userDetails['name']
        phone=userDetails['phone']
        address=userDetails['address']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name,phone,address,car,value) VALUES(%s,%s,%s,%s,%s)",(name,phone,address,'Mercedes-Benz','₹1800k'))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template("car2.html")

@app.route('/car3',methods=['GET','POST'])
def car3():
    if request.method=='POST':
        userDetails= request.form
        name= userDetails['name']
        phone=userDetails['phone']
        address=userDetails['address']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name,phone,address,car,value) VALUES(%s,%s,%s,%s,%s)",(name,phone,address,'Land Range Rover','₹2000k'))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template("car3.html")

@app.route('/car4',methods=['GET','POST'])
def car4():
    if request.method=='POST':
        userDetails= request.form
        name= userDetails['name']
        phone=userDetails['phone']
        address=userDetails['address']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name,phone,address,car,value) VALUES(%s,%s,%s,%s,%s)",(name,phone,address,'Porsche 911','₹2000k'))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template("car4.html")

@app.route('/car5',methods=['GET','POST'])
def car5():
    if request.method=='POST':
        userDetails= request.form
        name= userDetails['name']
        phone=userDetails['phone']
        address=userDetails['address']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name,phone,address,car,value) VALUES(%s,%s,%s,%s,%s)",(name,phone,address,'Nissan X-Trail','₹1900k'))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template("car5.html")

@app.route('/car6',methods=['GET','POST'])
def car6():
    if request.method=='POST':
        userDetails= request.form
        name= userDetails['name']
        phone=userDetails['phone']
        address=userDetails['address']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name,phone,address,car,value) VALUES(%s,%s,%s,%s,%s)",(name,phone,address,'Ferrari 488','₹2000k'))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template("car6.html")

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue= cur.execute("SELECT * FROM users")
    if resultValue>0:
        userDetails= cur.fetchall()
        return render_template('users.html',userDetails=userDetails)

@app.route('/selling')
def selling():
    cur = mysql.connection.cursor()
    resultValue= cur.execute("SELECT * FROM sell")
    if resultValue>0:
        userDetails= cur.fetchall()
        return render_template('selling.html',userDetails=userDetails)


if __name__=="__main__":
    app.run(debug=True)

