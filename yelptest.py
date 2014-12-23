from operateDB import connectDB

def isCategory(obj,  cateName):
    if cateName in obj['categories']:
            return 1
    return 0

def isCity(obj,  cityName):
    if obj['city'] == cityName:
        return 1
    return 0

col = connectDB('yelp',  'business')['col']
items = col.find()
num = 0
for i in items:
    if i['review_count']>50 and isCategory(i, 'Restaurants') and isCity(i,  'Las Vegas'):
        print str(num) + '  ' + str(i['business_id'])
    num += 1

    
