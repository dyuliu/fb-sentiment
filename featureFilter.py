from operateDB import connectDB
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

def compactFilter():
    global items,  itemlist
    num = 0
    for k in items:
        for i in itemlist:
            if (len(i[0])<4):
                if (isSub(i[0], k['noun'])):
                    i[3].append(num)
                    if ((len(i[0])>1) and (compact(i[0],  k))):
                       i[3+1] += 1
        num+=1
        
    for i in itemlist:
        if (len(i[0])<4):
            i.append(frozenset(i[3]))
            
    for i in itemlist:
        if (len(i[0])>1 and len(i[0])<4):
            if (1.0*i[3+1]/len(i[3])>0.5):
                final.append(i)
                #print str(i[0])+" "+str(1.0*i[ci+1]/len(i[ci]))

def pureFilter():
    global itemlist,  final,  items
    for k in itemlist:
        if (len(k[0])==1):
            for i in final:
                if (len(i[0])>1 and len(i[0])<4):
                    if (k[0][0] in i[0]):
                        k[3+2] = k[3+2] - i[3+2]    
            if (1.0*len(k[3+2])/items.count() > 0.01):
                final.append(k)
                
    def mycmp2(a, b):
        if (a[2]<b[2]):
            return 1;
        else:
            return -1;            
    final.sort(cmp = mycmp2)
    
    for k in final:
        iCol.insert({'feature' : k[0:3]})
        #print str(k[0]) + " " + str(k[1]) + " " + str(k[2])

            
def initialization(oriDB,  oriCol,  insertDB,  insertCol,  minSupport):
    global oCol,  iCol,  tCol,  items,  item,  itemlist,  final
    oCol = connectDB(oriDB,  oriCol)['col']
    iCol = connectDB(insertDB,  insertCol)['col']
    tCol = connectDB('amazon_phone',  'co-orcurrence')['col']
    item = tCol.find_one({"minSupport": minSupport})['items']
    items = oCol.find()
    itemlist = []
    final = []
    for i in item:
        i.append([])
        i.append(0)
        itemlist.append(i)
    
    def mycmp1(a, b):
        if (a[1]>b[1]):
            return 1;
        else:
            return -1;    
    itemlist.sort(cmp=mycmp1)

def featureFilter(oriDB,  oriCol,  insertDB,  insertCol,  minSupport=0.03): 
    initialization(oriDB,  oriCol,  insertDB,  insertCol,  minSupport)
    
    compactFilter()
    pureFilter()
    

           

    
   
    

    
    
    
        
