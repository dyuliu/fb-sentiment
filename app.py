
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request
from product_feature_sentiment import SentimentOfFeature
from bson.objectid import ObjectId 

app = Flask(__name__)

import os 
import time,  datetime

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getdata', methods=['GET','POST'])
def getdata():
    
    productName = request.args['productName']
    #productName = request.form['productName']
    
    #productName = 'B000NKCO5Q'
    print "start Processing"
    data = SentimentOfFeature(productName)
    print "finished"
    #print data
    res = {'psentences':data['psentences'], 'nsentences':data['nsentences'],  'msentences':data['msentences'],
    'productName': productName,  'featureInfo':data['featureInfo']}
    return jsonify(res)
                
if __name__ == '__main__':
    app.run()



