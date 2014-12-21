from operateDB import *
from frequentPattern import frequentPattern
from featureFilter import featureFilter
from featureBasedSentiment import SentimentOfFeature

IDSet = ['B0009B0IX4', 'B0007WWAGI',  'B000GAO9T2',  'B000CQXHOS',  'B000RUPEOA',  'B000PCCLPU',  'B0006GFARG',  'B000EM0WGG',  'B000CORUSO',  'B0009W8DLC',  'B000GAZPZE',  'B00001W0EQ', 
'B0009W8DKI',  'B000GX9D9K',  'B000HBIUNG',  'B000BBE9C8',  'B000BD3210',  'B000EF3D4G',  'B00006ZCDS',  'B000GM8QI0',  'B0007W1K3C',  'B000BHAUSE',  'B0006BBHJ6',  'B00004W6Y6',  'B000H3Z2K8', 
'B0000B35K8', 'B000CQFMEQ' , 'B000FOKF42',  'B000R4J56O',  'B000GM50DO',  'B000BT4BRS',  'B000E9ZO8A',  'B000FL2E4Y',  'B000NGWKI6',  'B000O3EU0O',  'B000IBKVR8',  'B00004WIO4',  'B000H6QSNK', 
'B0002KZN1Y',  'B000NBWZ7C',  'B000BJDQ7O']


# preprocessing data
print 'extracting reviews'
extractReviews(IDSet,  'amazon',  'phone',  'amazon_phone',  'headsets')
print 'tagging reviews'
reviewTagged('amazon_phone',  'headsets',  'amazon_phone',  'headsetsTagged')
print 'extracting nouns'
extractNouns('amazon_phone',  'headsetsTagged',  'amazon_phone',  'headsetsNouns')



# frequentPattern(oriDB,  oriCol,  insertDB,  insertCol,  minSupport=0.01,  minConfidence=0.8):
print 'finding frequentPattern'
frequentPattern('amazon_phone',  'headsetsNouns',  'amazon_phone',  'co-orcurrence', 0.1)
frequentPattern('amazon_phone',  'headsetsNouns',  'amazon_phone',  'co-orcurrence', 0.05)
frequentPattern('amazon_phone',  'headsetsNouns',  'amazon_phone',  'co-orcurrence', 0.03)



# featureFilter(oriDB,  oriCol,  insertDB,  insertCol,  minSupport=0.03): 
print 'filtering features'
featureFilter('amazon_phone',  'headsetsNouns',  'amazon_phone',  'features',  0.03)




#def SentimentOfFeature(oriDB,  oriCol):
IDSet = ['B0009B0IX4', 'B0007WWAGI',  'B000GAO9T2',  'B000CQXHOS',  'B000RUPEOA',  'B000PCCLPU']

print 'Calculating Sentiment of each feature & sentence'
for id in IDSet:
    print id
    print len(SentimentOfFeature(id)['featureInfo'])
#see mongoDB:    amazon_phone.visData

