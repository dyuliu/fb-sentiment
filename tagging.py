#tagging
import nltk
import string

def getTag(sentence):
    sentence = nltk.word_tokenize(sentence)
    sentence = [w.lower().rstrip(string.punctuation).lstrip(string.punctuation)  for w in sentence]
    tagged = nltk.pos_tag(sentence)
    return tagged    
