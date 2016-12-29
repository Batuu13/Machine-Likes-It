import csv
import pymongo
import mli_lib as mli
import lda
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import sklearn.cluster.mean_shift_ as ms
import simplejson as json
client = pymongo.MongoClient('localhost', 27017)
db = client['ml']
shops_collection = db.get_collection("shops")

# Add Businesses


def insert_business():
    with open('yelp_academic_dataset_business.csv') as csvfile:
        reader_bus = csv.DictReader(csvfile)
        print(reader_bus.fieldnames)
        for row_bus in reader_bus:
            print(row_bus['city'])

        for row_bus in reader_bus:
            doc = {
                "_id": row_bus['business_id'],
                "name": row_bus['name'],
                "reviews": []
            }
            shops_collection.insert_one(document=doc)
           # shops_collection.ensureIndex({"business_id": row_bus['business_id']}, {'unique': 'true'})
    print("Adding is finished")


def insert_review():

    with open('yelp_academic_dataset_review.csv') as csvfile:
        reader_rev = csv.DictReader(csvfile)
        print(reader_rev.fieldnames)
        for row_rev in reader_rev:
            doc = {
                "user_id" : row_rev['user_id'],
                "text" : row_rev['text'],
                "stars": row_rev['stars'],
                "votes_funny": row_rev['votes.funny'],
                "votes_useful": row_rev['votes.useful'],
                "votes_cool": row_rev['votes.cool'],
                "date": row_rev['date']
            }
            filt = {"_id": row_rev['business_id']}
            upd = {
                '$addToSet' : {
                    'reviews' : doc
                }
            }
            shops_collection.find_one_and_update(filter=filt,update=upd)


def test():
    with open('yelp_academic_dataset_business.csv') as csvfile:
        reader_bus = csv.DictReader(csvfile)
        print(reader_bus.fieldnames)
        i = 0
        cities = {}
        for row_bus in reader_bus:
            city_name = row_bus['city']
            count = cities.get(city_name,-1)
            if count == -1:
                cities[city_name] = 1
            else:
                cities[city_name] += 1

        print(cities.values())

for id in mli.get_business_id_list(20):
    print(id)
reviews = mli.get_reviews_city("Phoenix", type="neg")
#mli.do_nmf(reviews[:1500])
print(len(reviews))
#mli.do_lda(reviews[:1000],n_features=2000,n_topics=20,maxdf=0.1,n_top_words=1,range=(2,2))
#mli.do_nmf(reviews[:100],n_features=2000,n_topics=1,maxdf=0.3,n_top_words=5,range=(1,4))