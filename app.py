from flask import Flask, render_template, session, request, redirect
from flask import Flask, jsonify, render_template, url_for
from flask.templating import render_template_string
from pymongo import MongoClient
import os
import pandas as pd
import csv
import requests

app = Flask(__name__)

client = MongoClient("mongodb+srv://binay_99:Watson%4099@bdat1007.n5kgy.mongodb.net/test?authSource=admin&replicaSet=atlas-124cba-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")
db=client["Guitar"]
mycol=db["Guitar_Info"]

def csv_to_json(filename,header=None):
    data = pd.read_csv(filename, header=header)
    return data.to_dict('records')

@app.route("/")
def index():
    guitar_list=mycol.find()
    return render_template('index.html',guitar_list = guitar_list)

@app.route('/fileupload')
def upload_file():
   return render_template('fileupload.html')

@app.route("/uploader",methods=['POST','GET'])
def fileupload():
    if request.method == 'POST':
        f = request.files['filename']
        if f.filename != '':
            f.save(f.filename)
            mycol.insert_many(csv_to_json(f.filename,header=0))
            return "file uploaded successfully"
    else:
        return render_template('fileupload.html')
@app.route("/form")
def form():
    category_list=mycol.distinct("Category")
    return render_template('form.html',category_list=category_list)

@app.route("/formpost",methods=['POST','GET'])
def formpost():
    if request.method == 'POST':
       category= request.form['Category']
       name = request.form['Name']
       price = request.form['Price']
       mrp = request.form['maxprice']
       lprice = request.form['lowprice']
       ratings = request.form['ratings']
       reviews = request.form['reviews']
       mydict = {"Category":category,"Name":name,"PRICE":price,"MSRP":mrp,"LOWPRICE":lprice,"RATINGS":ratings,"REVIEWS":reviews}
       message=''
       try:
           mycol.insert_one(mydict)
           message="Data added successfully!"
       except:
            message="Something else gone wrong!!"
            return message
       guitar_list=mycol.find()
       return render_template('index.html',message=message,guitar_list=guitar_list)
if __name__ == "__main__":
    app.run(debug=True)


