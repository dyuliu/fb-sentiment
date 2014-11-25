from pymongo import MongoClient
from bson.objectid import ObjectId 
from tagging import getTag

def loadSet():
    file_pos = open('positive-words.txt', 'rU')
    file_neg = open('negative-words.txt', 'rU')
    file_nav = open('negation-words.txt', 'rU')
    
    global positives
    global negatives
    global negations
    
    for line in file_pos:
            line = line.strip().rstrip(',')                         # Remove trailing comma
            positives.add(line)
    
    for line in file_neg:
            line = line.strip().rstrip(',')                         # Remove trailing comma
            negatives.add(line)
    
    for line in file_nav:
            line = line.strip().rstrip(',')                         # Remove trailing comma
            negations.add(line)

def getSentences(sentences):
    snum = 0
    sent = []
    sent_set = []
    for s in sentences:
        sent.append(s)
        sent_set.append(set())
        for w in s['text']:
            sent_set[snum].add(w[0])
        snum += 1
        #if snum>2:
        #   break

    return sent,  sent_set
    
def getNeighbour(sentence,  position,  ran=3):
    left = max(0,  position-ran)
    right = min(len(sentence)-1,  position+ran)
    nb = []
    for i in range(left,  right+1):
        nb.append(sentence[i])
    return nb
        
def find_negation_word(neighbour):
    for i in neighbour:
        if i[0] in negations:
            return True
    return False
    
def judge(sentence):
    posemo = 0
    negemo = 0
    
    position = 0
    for word in sentence['text']:
            word = word[0]
            neighbour = getNeighbour(sentence['text'],  position,  3)
            negOrient = find_negation_word(neighbour)
            position += 1
            if word in positives:
                if negOrient:
                    negemo +=1
                else:
                    posemo +=1
            elif word in negatives:
                if negOrient:
                    posemo +=1
                else:
                    negemo += 1
    
    return {'sentiment': posemo-negemo,  'positive': posemo,  'negative':negemo}

def Sentiment_Judge(sentences):
    global sentiments,  totpos,  totneg,  totmid
    num = 0
    for i in sentences:
        sentiments.append(judge(i))
        #print sentiments[num]
        if sentiments[num]['sentiment']<0:
            totneg += 1
        elif sentiments[num]['sentiment']>0:
            totpos += 1
        elif (sentiments[num]['sentiment']==0):
            totmid += 1
        #if ( num % 5000 == 0):
        #    print num
        num +=1
 
def isSub(sub, sup):
    if (sup.issuperset(sub)):
        return True
    else:
        return False

def feature_in(feature,  wordsset):
    for w in wordsset:
        if feature==w[0]:
            return True
    return False
        
def Calc_feature(feature,  sentence,  snum): 
    global sentences_set
    if isSub(set(feature),  sentences_set[snum]):
        wpos = 0
        leftp = -1
        rightp = -1
        tpositive = 0
        tnegative = 0
        posfnum = [0]*len(feature)
        negfnum = [0]*len(feature)
        for w in sentence['text']:
            
            sf = 0
            for f in feature:
                if f == w[0]:
                    nb = getNeighbour(sentence['text'],  wpos,  3)
                    countp = False
                    countn = False
                    for word in nb:
                        word = word[0]
                        if (word in positives and not countp):
                            posfnum[sf] += 1
                            countp = True
                        if (word in negatives and not countn):
                            negfnum[sf] +=1
                            countn = True
                sf += 1
                
            if (w[0] in positives or w[0] in negatives):
                
                nb = getNeighbour(sentence['text'],  wpos,  3)
                fin = False
                for f in feature:
                    if feature_in(f,  nb):
                        fin = True
                        break
                if fin:
                    word = w[0]
                    if (word in positives):
                        neighbour = getNeighbour(sentence['text'],  wpos,  3)
                        if (find_negation_word(neighbour)):
                            tnegative += 1
                        else:
                            tpositive += 1
                    elif (word in negatives):
                        neighbour = getNeighbour(sentence['text'],  wpos,  3)
                        if (find_negation_word(neighbour)):
                            tpositive += 1
                        else:
                            tnegative += 1

            wpos += 1       
        
        return tpositive - tnegative,  tpositive,  tnegative,  min(posfnum),  min(negfnum)
    
    return 0, 0, 0, 0, 0  
    
def Feature_Judge(sentences):
    global features
    
    for f in features:
        f.append({'pnum':0,  'nnum':0,  'positive_set':set(),  'negative_set':set(),  'pval':0,  'nval':0,  'negfnum':0,  'posfnum':0})
       # print f

    snum =0
    for s in sentences:
        for f in features:
            pon = Calc_feature(f[0],  s,  snum)
            if (pon[0] > 0):
                f[3]['pnum'] += 1
                f[3]['positive_set'].add(snum) 
            elif (pon[0] < 0):
                f[3]['nnum'] += 1
                f[3]['negative_set'].add(snum) 
            f[3]['pval'] += pon[1]
            f[3]['nval'] += pon[2]
            f[3]['posfnum'] += pon[3]
            f[3]['negfnum'] += pon[4]
        snum += 1
        
def SentimentOfFeature(productName):
    
    result = {}
    
    client = MongoClient('localhost',  27017)
    db = client.amazon
    str_col = 'phone_tag_'+ productName
    col = db[str_col]
    
    global positives,  negatives,  negations
    positives = set()
    negatives = set()
    negations = set()
    loadSet()
    
    global sentences, sentences_set
    sentences = col.find()
    print 'Total number of reviews: ' + str(sentences.count())
    myget = getSentences(sentences)
    sentences = myget[0]
    sentences_set = myget[1]
    
    global sentiments
    sentiments = []
    fcol = db.phone_features
    iter_features = fcol.find()
    
    global features
    features = []
    for f in iter_features:
        features.append(f['feature'])
     
    global totpos,  totneg,  totmid
    totpos = 0  
    totneg = 0 
    totmid = 0 
    print "sentences sentiment judging"
    Sentiment_Judge(sentences)

    result['psentences'] = totpos
    result['nsentences'] = totneg
    result['msentences'] = totmid

    print "sentiment based on feature"
    Feature_Judge(sentences)
    feature_info = []
    for f in features:
        #print str(f[0]) + str(f[3]['pnum']) + str(f[3]['nnum'])
        if (1.0*(f[3]['pnum'] + f[3]['nnum'])/len(sentences))>0.02:
           feature_info.append({'feature':f[0],  'support':f[2],  'positive_review_Num':f[3]['pnum'],  'negative_review_Num':f[3]['nnum'],  'positiveVal':f[3]['pval'],  'negativeVal':f[3]['nval'],  'posNum':f[3]['posfnum'],'negNum':f[3]['negfnum']})

    def mycmp(a, b):
        if (a['support']<b['support']):
            return 1;
        else:
            return -1;
            
    feature_info.sort(cmp = mycmp)
    
    result['featureInfo'] = feature_info
    return result


'''
#print SentimentOfFeature('B000NKCO5Q')['featureInfo'][0]
iclient = MongoClient('localhost',  27017)
idb = iclient.amazon
icol = idb.phone_vis

productSet = ['B0007WWAGI',  'B0009B0IX4', 'B000CQXHOS', 'B000GAO9T2', 'B000NKCO5Q', 'B000RUPEOA']
#productSet = ['B000NKCO5Q']
for productName in productSet:
    data = SentimentOfFeature(productName)
    res = {'psentences':data['psentences'], 'nsentences':data['nsentences'],  'msentences':data['msentences'],
        'productName': productName,  'featureInfo':data['featureInfo']}
    icol.insert(res)
'''  
