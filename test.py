from operateDB import connectDB
from flask import Flask, jsonify
import json

col = connectDB('amazon',  'phone')['col']
items = col.find()
data = []
num = 0
for i in items:
    data.append(i)
    if (num >2):
        break
    num += 1
    print jsonify(**data)
with open('test.json', 'w+') as outfile:
  json.dump(data, outfile)
