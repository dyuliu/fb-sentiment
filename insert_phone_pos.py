from pymongo import MongoClient
from tagging import getTag

if __name__ == "__main__":
    client = MongoClient('localhost',  27017)
    db = client.amazon
    col = db.phone_tag
    icol = db.phone_only_pos
    items = col.find()
    num = 0
   # i = col.find_one()
   # words = i['text']
 

    for item in items:
        words = item['text']
        length = len(words)
        review = []
        review_pos = []
        for i in range(length):
            if ((len(words[i][0])>1) and (words[i][1] == "NN" or words[i][1] == "NNS")):
                review.append(words[i][0])
                review_pos.append(i)
        tmp_item = {"noun":  review,  "pos":  review_pos}
        icol.insert(tmp_item)

    
