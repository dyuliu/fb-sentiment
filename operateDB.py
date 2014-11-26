from pymongo import MongoClient
from tagging import getTag

def connectDB(dbName,  colName):
    client = MongoClient('localhost',  27017)
    db = client[dbName]
    col = db[colName]
    return {'db':db,  'col':col}
    
    
def extractReviews(IDSet,  oriDB,  oriCol,  insertDB,  insertCol):    
    oCol = connectDB(oriDB,  oriCol)['col']
    iCol = connectDB(insertDB,  insertCol)['col']
    for id in IDSet:
        items = oCol.find({'product/productId': id})
        for item in items:
            iCol.insert(item)
          
        
def reviewTagged(oriDB,  oriCol,  insertDB,  insertCol):
    oCol = connectDB(oriDB,  oriCol)['col']
    iCol = connectDB(insertDB,  insertCol)['col']
    
    items = oCol.find()
    print items.count()
    for item in items:
        iCol.insert({"_id": item['_id'], "productId":item['product/productId'], "score":item['review/score'], "text": getTag(item['review/text'])})
            
def extractNouns(oriDB,  oriCol,  insertDB,  insertCol):
    oCol = connectDB(oriDB,  oriCol)['col']
    iCol = connectDB(insertDB,  insertCol)['col']
    items = oCol.find()
    for item in items:
        sentence = item['text']
        length = len(sentence)
        words = []
        words_pos = []
        for i in range(length):
            if ((len(sentence[i][0])>1) and (sentence[i][1] == "NN" or sentence[i][1] == "NNS")):
                words.append(sentence[i][0])
                words_pos.append(i)
        iCol.insert({"noun":  words,  "pos":  words_pos})
