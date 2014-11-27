from operateDB import connectDB
from bson.objectid import ObjectId 
from tagging import getTag

def loadSet():
    file_pos = open('wordstat/positive-words.txt', 'rU')
    file_neg = open('wordstat/negative-words.txt', 'rU')
    file_nav = open('wordstat/negation-words.txt', 'rU')
    
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
            return True,  i[0]
    return False,  i[0]
    
def judge(sentence):
    posemo = 0
    negemo = 0
    
    position = 0
    for word in sentence['text']:
            word = word[0]
            neighbour = getNeighbour(sentence['text'],  position,  3)
            negOrient = find_negation_word(neighbour)[0]
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
        if sentiments[num]['sentiment']<0:
            totneg += 1
        elif sentiments[num]['sentiment']>0:
            totpos += 1
        elif (sentiments[num]['sentiment']==0):
            totmid += 1
        num +=1
    finalResult['psentences'] = totpos
    finalResult['nsentences'] = totneg
    finalResult['msentences'] = totmid
 
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
        posAdj = []
        negAdj = []
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
                        negationword = find_negation_word(neighbour)
                        if (negationword[0]):
                            tnegative += 1
                            negAdj.append(negationword[1]+' '+word)
                        else:
                            tpositive += 1
                            posAdj.append(word)
                    elif (word in negatives):
                        neighbour = getNeighbour(sentence['text'],  wpos,  3)
                        negationword = find_negation_word(neighbour)
                        if (negationword[0]):
                            tpositive += 1
                            posAdj.append(negationword[1]+' '+word)
                        else:
                            tnegative += 1
                            negAdj.append(word)

            wpos += 1       
        
        return tpositive - tnegative,  tpositive,  tnegative,  min(posfnum),  min(negfnum),  posAdj,  negAdj,  True
    
    return 0, 0, 0, 0, 0, [], [], False
    
def Feature_Judge(sentences):
    global sentiments,  features,  featureVis,  finalResult
    
    for f in features:
        f.append({'pnum':0,  'nnum':0,  'positive_set':set(),  'negative_set':set(),  'pval':0,  'nval':0,  'negfnum':0,  'posfnum':0,  'posAdj':[],  'negAdj':[]})
       # print f

    def listtostr(feature):
        s = ''
        for f in feature:
            s = s + ' ' +f
        return s[1:]

    snum =0
    for s in sentences:
        featureVis.append({'reviewID': s['_id'],  'score': s['score'],  'sentiment':sentiments[snum]['sentiment'],'pnum':sentiments[snum]['positive'], 'nnum':sentiments[snum]['negative'], 'features':[]})
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
            f[3]['posAdj'] += pon[5]
            f[3]['negAdj'] += pon[6]
            if pon[7]:
                featureVis[snum]['features'].append({listtostr(f[0]):  {'pos':pon[1],  'neg':pon[2]}})
        
        snum += 1
    
    feature_info = []
    for f in features:
        #print str(f[0]) + str(f[3]['pnum']) + str(f[3]['nnum'])
        if (1.0*(f[3]['pnum'] + f[3]['nnum'])/len(sentences))>0.05:
           feature_info.append({'feature':f[0],  'support':f[2],  'positive_review_Num':f[3]['pnum'],  'negative_review_Num':f[3]['nnum'],  'positiveVal':f[3]['pval'],  'negativeVal':f[3]['nval'],  'posNum':f[3]['posfnum'],'negNum':f[3]['negfnum'], 'posAdj':f[3]['posAdj'], 'negAdj':f[3]['negAdj']})

    def mycmp(a, b):
        if (a['support']<b['support']):
            return 1;
        else:
            return -1;            
    feature_info.sort(cmp = mycmp)
    finalResult['featureInfo'] = feature_info
    finalResult['featureVis'] = featureVis

def initialization(productId,  oriDB,  oriCol,   featureDB,  featureCol):
    global positives,  negatives,  negations,  sentences,  sentences_set, sentiments,  features,  totpos,  totneg,  totmid,  finalResult, featureVis,  iCol
    oCol = connectDB(oriDB,  oriCol)['col']
    iCol = connectDB('amazon_phone',  'visData')['col']
    totpos = 0  
    totneg = 0 
    totmid = 0 
    sentiments = []
    features = []
    featureVis = []
    finalResult = {}
    positives = set()
    negatives = set()
    negations = set()
    loadSet()
    sentences = oCol.find({'productId': productId})
    print 'Total number of reviews: ' + str(sentences.count())
    myget = getSentences(sentences)
    sentences = myget[0]
    sentences_set = myget[1]
    
    fCol = connectDB(featureDB,  featureCol)['col']
    iter_features = fCol.find()
    
    for f in iter_features:
        features.append(f['feature'])


def SentimentOfFeature(productId,  oriDB='amazon_phone',  oriCol='headsetsTagged',  insertDB='amazon_phone',  insertCol='visData',  featureDB='amazon_phone',  featureCol='features'):
    initialization(productId,  oriDB,  oriCol,  featureDB,  featureCol)
    #print "sentences sentiment judging"
    Sentiment_Judge(sentences)
    #print "sentiment based on feature"
    Feature_Judge(sentences)
    iCol = connectDB('amazon_phone',  'visData')['col']
    res = {'psentences':finalResult['psentences'], 'nsentences':finalResult['nsentences'],  'msentences':finalResult['msentences'],
    'productName': productId,  'featureInfo':finalResult['featureInfo'],  'featureVis':finalResult['featureVis']}
    iCol.insert(res)
    return finalResult




