from pymongo import MongoClient
from bson.objectid import ObjectId 
import os
 
def isSub(sub, sup):
    for i in sub:
        if (not(i in sup)):
            return False
    return True
            
def compact(sub,  sup):
    pos = []
    for i in sub:
        pos.append(sup['pos'][sup['noun'].index(i)])
    pos.sort()
    for i in range(1,  len(pos)):
        if (pos[i]-pos[i-1]>3):
            return False
    return True


#def purefilter():   
    
def mycmp(a, b):
    if (a[1]>b[1]):
        return 1;
    else:
        return -1;

def mycmp2(a, b):
    if (a[2]<b[2]):
        return 1;
    else:
        return -1;

if __name__ == "__main__":
 
    client = MongoClient('localhost',  27017)
    db = client.amazon
    col = db.phone_only_pos
    tcol = db.co_occurence
    items = col.find()
    item = tcol.find_one({"_id": ObjectId('5471d285338a2a5617267f72')})
    
    #print item['items'][1523]
    #print len(item['items'])

    ci = 3;
    itemlist = []

    for i in item['items']:
        i.append([])
        i.append(0)
        itemlist.append(i)
        
    itemlist.sort(cmp=mycmp)
    
    num = 0
    for k in items:
        for i in itemlist:
            if (len(i[0])<4):
                if (isSub(i[0], k['noun'])):
                    i[ci].append(num)
                    if ((len(i[0])>1) and (compact(i[0],  k))):
                       i[ci+1] += 1
        num+=1
    
    for i in itemlist:
        if (len(i[0])<4):
            i.append(frozenset(i[ci]))
        
            #os.system("pause")
                
    final = []
    for i in itemlist:
        if (len(i[0])>1 and len(i[0])<4):
            if (1.0*i[ci+1]/len(i[ci])>0.5):
                final.append(i)
                #print str(i[0])+" "+str(1.0*i[ci+1]/len(i[ci]))
           
    for k in itemlist:
        if (len(k[0])==1):
            for i in final:
                if (len(i[0])>1 and len(i[0])<4):
                    if (k[0][0] in i[0]):
                        k[ci+2] = k[ci+2] - i[ci+2]    
            if (1.0*len(k[ci+2])/items.count() > 0.01):
                final.append(k)
                
    final.sort(cmp = mycmp2)
    fcol = db.phone_features
    for k in final:
        fcol.insert({'feature' : k[0:3]})
        print str(k[0]) + " " + str(k[1]) + " " + str(k[2])
    
   
    
    
    
        
