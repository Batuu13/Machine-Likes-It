import csv
import pymongo
import mli_lib as mli
import operator
import ast
import lda
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import sklearn.cluster.mean_shift_ as ms
import simplejson as json
client = pymongo.MongoClient('localhost', 27017)
db = client['ml']
shops_collection = db.get_collection("shops")
occurance = {}


def add_dict(topics):
    for topic in topics:
        for word in topic:
            count = occurance.get(word, -1)
            if count == -1:
                occurance[word] = 1
            else:
                occurance[word] += 1
total_review = 0 ;
test_size = 6000
k = 0
i = 0


print(i)
for id in mli.get_business_id_list(20):
    if(k >= test_size):
        break
    reviews = mli.get_reviews_business(id['_id'], type="pos")
    print("#",k," ", id['_id'], len(reviews))
    if (len(reviews) < 5):
        print("Passed!")
        continue
    topics = mli.do_lda(reviews, n_features=2000, n_topics=1, maxdf=0.95, n_top_words=15, range=(1, 1),isSplit=1)
    add_dict(topics[0])
    k +=1
    total_review += len(reviews)

sorted_x = sorted(occurance.items(), key=operator.itemgetter(1), reverse=True)
print(sorted_x)
print("Total Review: ",total_review)

toWrite = '\n\nTotal Review:' + str(total_review) + ' \n' + str(sorted_x)
with open("lda_result_pos.txt", "a") as testfile:
    testfile.write(toWrite)



#mli.do_nmf(reviews[:1000],n_features=2000,n_topics=1,maxdf=0.95,n_top_words=10,range=(1,3),isSplit=1)