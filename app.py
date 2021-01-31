from flask import Flask, render_template, session, request, redirect
from flask import Flask, jsonify, render_template, url_for
from flask.templating import render_template_string
from pymongo import MongoClient
from bson import ObjectId
import os
import pandas as pd
import csv
import requests

app = Flask(__name__)

client = MongoClient("mongodb+srv://binay_99:Watson%4099@bdat1007.n5kgy.mongodb.net/test?authSource=admin&replicaSet=atlas-124cba-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")
db=client["Guitar"]
mycol=db["Guitar_Info"]
mycategory=db["Guitar_Category"]
def csv_to_json(filename,header=None):
    data = pd.read_csv(filename, header=header)
    return data.to_dict('records')

# Index
@app.route("/")
def index():
    guitar_list=mycol.find()
    return render_template('index.html',guitar_list = guitar_list)
# Index

# File Upload
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
            mycategory.insert_many(csv_to_json(f.filename,header=0))
            message="File Uploaded Successfully"
            guitar_list=mycol.find()
            return render_template('index.html',message=message,guitar_list=guitar_list)
    else:
        return render_template('fileupload.html')

# FIle Upload

# Add New Category
@app.route("/AddCategory")
def AddCategory():
    return render_template('AddCategory.html')

@app.route("/AddCategoryp",methods=['POST','GET'])
def AddCategoryp():
    if request.method == 'POST':
       category= request.form['Name']
       mydict = {"Category":category}
       message=''
       try:
           mycategory.insert_one(mydict)
           message="Category added successfully!"
       except:
            message="Something else gone wrong!!"
            return message
       guitar_list=mycol.find()
       return render_template('index.html',message=message,guitar_list=guitar_list)
# Add New Category

# Add New Form
@app.route("/form")
def form():
    category_list=mycategory.distinct("Category")
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
       mydict = {"Category":category,"Name":name,"Price":price,"MSRP":mrp,"LowPrice":lprice,"Ratings":ratings,"Reviews":reviews}
       message=''
       try:
           mycol.insert_one(mydict)
           message="Data added successfully!"
       except:
            message="Something else gone wrong!!"
            return message
       guitar_list=mycol.find()
       return render_template('index.html',message=message,guitar_list=guitar_list)
# Add New Form

# Read Form
@app.route("/view")
def view():
    id = request.values.get("_id")
    data_info = mycol.find_one({"_id": ObjectId(id)})
    return render_template('view.html',data_info=data_info)
# Read Form

# Edit form

@app.route("/edit")
def edit():
    id = request.values.get("_id")
    data_info = mycol.find_one({"_id": ObjectId(id)})
    return render_template('edit.html',data_info=data_info)

@app.route("/updatep", methods=['POST'])
def updatep ():
    #Updating a data with various references
    category=request.values.get("Category")
    name=request.values.get("Name")
    price=request.values.get("Price")
    mrp=request.values.get("maxprice")
    lp=request.values.get("lowprice")
    ratings=request.values.get("ratings")
    reviews=request.values.get("reviews")
    id=request.values.get("_id")
    mycol.update({"_id":ObjectId(id)}, {'$set':{ "Category":category,"Name":name, "Price":price, "MRSP":mrp, "LowPrice": lp,"Ratings":ratings,"Reviews":reviews}})    
    message="Data updated successfully!"
    guitar_list=mycol.find()
    return render_template('index.html',message=message,guitar_list=guitar_list)

# Edit Form

# Delete Form
@app.route("/remove")
def remove ():
    #Deleting a data with various references
    key=request.values.get("_id")
    mycol.remove({"_id":ObjectId(key)})
    message="Data Deleted successfully!"
    guitar_list=mycol.find()
    return render_template('index.html',message=message,guitar_list=guitar_list)
# Delete Form
if __name__ == "__main__":
    app.run(debug=True)


