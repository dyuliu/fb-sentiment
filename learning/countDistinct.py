from pymongo import MongoClient
from tagging import getTag

def mycmp(a, b):
    if (a['num']>b['num']):
        return 1
    else:
        return -1    

if __name__ == "__main__":
    client = MongoClient('localhost',  27017)
    db = client.amazon
    col = db.phone
    #items = col.distinct('product/productId')
    
   #col.aggregate([{$group : {_id : "$product/productId", num : {$sum : 1}}}])
    
    items = list(col.aggregate({"$group": {"_id": '$product/productId',  "num": {"$sum":  1}}})['result'])
    
    
    #items = list(col.aggregate({"$group": {"_id": '$product/productId',  "num": {"$sum":  1}}})['result'])
    #print items    
    items.sort(cmp = mycmp)
    inum =0
    f = open('itemlist.txt',  'w+')
    for item in items:
        item['title'] = col.find_one({'product/productId': item['_id']})['product/title']
        f.write(str(item)+'\n')
        #print str(item)
        if (inum > 1000):
            break
        inum += 1
    f.write(str(len(items))+'\n')
   # print len(items)
    f.close()
    '''
    print ''
    inum = 0
    rs = []
    for item in items:
        #print col.count({"product/productId": item})
        
        f = col.find({"product/productId": item})
        rs.append((item , f.count()))
        if (inum % 20 == 0):
            print inum
        inum += 1

    rs.sort(cmp = mycmp)
    inum =0
    for i in rs:
        print i
        if (inum >5):
            break;
        inum += 1

    #db.runCommand({"distinct":"phone",  "key":"product/productId"})
    '''
