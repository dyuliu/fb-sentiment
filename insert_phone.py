from pymongo import MongoClient
from tagging import getTag

def insert_phone_tag(productName,  complete):
    client = MongoClient('localhost',  27017)
    db = client.amazon
    col = db.phone
    
    if (complete):
        items = col.find()
        str_col = 'phone_tag'
    else:
        items = col.find({'product/productId': productName})
        str_col = 'phone_tag_' + productName
        
    icol = db[str_col]
    
    print str_col
    print items.count()
    for item in items:
        icol.insert({"text": getTag(item['review/text'])})  
            





#insert_phone_tag('B0007WWAGI' ,  0)
insert_phone_tag('B0009B0IX4' ,  0)
insert_phone_tag('B000CQXHOS' ,  0)
insert_phone_tag('B000GAO9T2' ,  0)
insert_phone_tag('B000NKCO5Q' ,  0)
insert_phone_tag('B000RUPEOA' ,  0)
