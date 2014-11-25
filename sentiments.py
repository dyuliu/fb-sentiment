from pymongo import MongoClient

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
        if (snum % 5000 == 0):
            #break
            print snum
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

def Calc_feature(feature,  sentence,  snum): 
    global sentences_set
    if isSub(set(feature),  sentences_set[snum]):
        wpos = 0
        leftp = -1
        rightp = -1
        for w in sentence['text']:
            
            for f in feature:
                if (w[0] == f):
                    if (leftp>wpos or leftp == -1):
                        leftp = wpos
                    if (rightp<wpos or rightp == -1):
                        rightp = wpos
            #print rightp
            wpos += 1       
        
        tpositive = 0
        tnegative = 0
        for p in range(max(leftp-3, 0),  min(rightp+3, len(sentence['text'])-1)):
            word = sentence['text'][p][0]
            if (word in positives):
                neighbour = getNeighbour(sentence['text'],  p,  3)
                if (find_negation_word(neighbour)):
                    tnegative += 1
                else:
                    tpositive += 1
            elif (word in negatives):
                neighbour = getNeighbour(sentence['text'],  p,  3)
                if (find_negation_word(neighbour)):
                    tpositive += 1
                else:
                    tnegative += 1
        return tpositive - tnegative    
    
    return 0      
    
def Feature_Judge(sentences):
    global features
    
    for f in features:
        f.append({'positive':0,  'negative':0,  'positive_set':set(),  'negative_set':set()})
       # print f

    snum =0
    for s in sentences:
        for f in features:
            pon = Calc_feature(f[0],  s,  snum)
            if (pon >= 1):
                f[3]['positive'] += 1
                f[3]['positive_set'].add(snum) 
            elif (pon <=-1):
                f[3]['negative'] += 1
                f[3]['negative_set'].add(snum) 
        snum += 1
        
if __name__ == "__main__":
    
    positives = set()
    negatives = set()
    negations = set()
    totpos = 0
    totneg = 0
    totmid = 0
    
    loadSet()
    
    #print len(positives)
    #print len(negatives)
    #print negations
    
    client = MongoClient('localhost',  27017)
    db = client.amazon
    col = db.phone_tag
    sentences = col.find()
    myget = getSentences(sentences)
    sentences = myget[0]
    sentences_set = myget[1]
    
    #scol = db.phone_reviews_text
    #scol.insert({'sentences': str(sentences)})
    #exec "abc = " + str(sentences)
   
    sentiments = []
    fcol = db.phone_features
    iter_features = fcol.find()
    features = []
    for i in iter_features:
        features.append(i['feature'])
     
    print "sentences sentiment judging"
    Sentiment_Judge(sentences)
    print 'total positive: ' + str(totpos)
    print 'total negative: ' + str(totneg)
    print 'total neutral: ' + str(totmid)

    print "sentiment based on feature"
    Feature_Judge(sentences)
    for f in features:
        if (1.0*(f[3]['positive'] + f[3]['negative'])/len(sentences))>0.02:
            print str(f[0]) +  ' s: ' + str(f[2]) +' p: ' + str(f[3]['positive']) + ' n: ' + str(f[3]['negative'])     

    
