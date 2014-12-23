from operateDB import *
from frequentPattern import frequentPattern
from featureFilter import featureFilter
from featureBasedSentiment import SentimentOfFeature

'''
# Training Set:   IDSet  
IDSet = ['fjaQ3Ixkofh8xGhklUtDnA',  'HLWtNcf3l-wKb6v9duteMQ']

# preprocessing data
print 'extracting reviews'
extractReviews(IDSet,  'yelp',  'review',  'yelp_food',  'restaurant')
print 'tagging reviews'
reviewTagged('yelp_food',  'restaurant',  'yelp_food',  'restaurantTagged')
print 'extracting nouns'
extractNouns('yelp_food',  'restaurantTagged',  'yelp_food',  'restaurantNouns')


# frequentPattern(oriDB,  oriCol,  insertDB,  insertCol,  minSupport=0.01,  minConfidence=0.8):
print 'finding frequentPattern'
frequentPattern('yelp_food',  'restaurantNouns',  'yelp_food',  'co-orcurrence', 0.1)
frequentPattern('yelp_food',  'restaurantNouns',  'yelp_food',  'co-orcurrence', 0.05)
frequentPattern('yelp_food',  'restaurantNouns',  'yelp_food',  'co-orcurrence', 0.03)



# featureFilter(oriDB,  oriCol,  insertDB,  insertCol,  minSupport=0.03): 
print 'filtering features'
featureFilter('yelp_food',  'restaurantNouns',  'yelp_food',  'features',  0.05)
'''




#def SentimentOfFeature(oriDB,  oriCol):
IDSet = ['fjaQ3Ixkofh8xGhklUtDnA']

print 'Calculating Sentiment of each feature & sentence'
for id in IDSet:
    print id
    print len(SentimentOfFeature(id)['featureInfo'])
#see mongoDB:    amazon_phone.visData

