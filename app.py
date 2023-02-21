
from flask import Flask,render_template,request,redirect,url_for
import mysql.connector as c
import database as db
import app
from fileinput import filename
import pymongo
import pandas as pd
con = c.connect(host = "localhost",user = "root",password = "honeychandu",database = 'project')
cursor = con.cursor()
app = Flask(__name__)
@app.route('/',methods = ['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template('Ticket.html')
    return render_template('Ticket.html')
@app.route('/listBus',methods = ['GET','POST'])
def book():
    if request.method == 'POST':
        route = request.form['route']
        type = request.form['type']
        date = request.form['date']
        data = db.book(route,type,date)
        return render_template('show.html',table = data)
    return render_template('Ticket.html')

@app.route('/signup',methods = ['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    name   = request.form['fullname']
    email  = request.form['email']
    mobile = request.form['number']
    gender = request.form['gender']
    pass1  = request.form['password1']
    pass2  = request.form['password2']
    data   = db.signup_val()
    if email in data:
        return render_template('signup.html',msg = 'Looks like you are already registered')
    elif pass1 == pass2:
        insert = db.signup(name,email,mobile,gender,pass1)
        return render_template('signup.html',msg = insert)
    else:
        return render_template('signup.html',msg ='Password Miss match')
@app.route('/signin', methods = ['GET','POST'])
def signin():
    if request.method=='GET':
        return render_template('signin.html')
    email = request.form['email']
    passw = request.form['password']
    data = db.signin(email) 
    signin.custid = db.custidf(email) 
    user = db.name(email)
    if passw in data:
        return render_template('Ticket.html')
    else:
        return render_template('signin.html',msg =data)
    



@app.route('/BookBus',methods = ['GET','POST'])
def bookbus():
    if request.method == 'POST':
        bookbus.id = request.form['ID']
        data = db.bookbus(bookbus.id)
        gst = float((data[0]/100)*11) 
        service_charge = int(20)
        total = float(data[0]+gst+service_charge)
        return render_template('bookbus.html',Price = data,gst=gst,charge = service_charge,total =total)
    return render_template('show.html')
@app.route('/disticket',methods = ['GET','POST'])
def displayticket():
    if request.method == 'GET':
        cursor = con.cursor()
        cursor.execute("""
        select signup.s_no,signup.fullname,signup.mobile,signup.gender,buses.BusName,buses.BusNum,buses.route,buses.Date,buses.depTime,buses.type,buses.TotalTime from signup join buses where signup.email = '{ID}' and buses.s_no = {busid};

    """.format(ID = 'prathap@gmail.com',busid = 1))
        table =  cursor.fetchall()
        con.commit()
        cursor.close
        return render_template('disticket.html',table = table)

if __name__ =='__main__':
    app.run(port = 5000,debug = True)
    print("welcome!!!!!!!!")
    uri = "mongodb://localhost:27017/";
    client = pymongo.MongoClient(uri)
    print(client)
    mydb = client["nsrit"]
    info = mydb["details"]