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

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" | ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()


def get_occurance(data):
    words = {}
    for sent in data:
        for word in str(sent).split(" "):
            count = words.get(word, -1)
            if count == -1:
                words[word] = 1
            else:
                words[word] += 1
    return words

def lda_test():
    business_size = 350
    id = "b'KayYbHCt-RkbGcPdGOThNg'"
    reviews = []
    filt = {"_id": id}
    js = shops_collection.find(filt).next()
    i=0
    '''for business in js:
        if i >= business_size:
            break
        for i in range(len(business['reviews'])):
            reviews.append(mli.correctify(business['reviews'][i]['text']))

        i += 1
    '''
    for i in range(len(js['reviews'])):
        raw = str(mli.correctify(js['reviews'][i]['text']))
        splitted = str(mli.correctify(js['reviews'][i]['text'])).split(".")
        #reviews.append(raw)
        for sent in splitted:
            reviews.append(sent)


    n_samples = 2000
    n_features = 1000
    n_topics = 10
    n_top_words = 5

    tfidf_vectorizer = TfidfVectorizer(max_df=0.90,
                                       max_features=n_features,
                                       stop_words='english',ngram_range=(1,4))
    tfidf = tfidf_vectorizer.fit_transform(reviews)
    tf_vectorizer = CountVectorizer(
                                    max_features=n_features,
                                    stop_words='english',ngram_range=(1,1))
    tf = tf_vectorizer.fit_transform(reviews)
    nmf = NMF(n_components=n_topics, random_state=1,
              alpha=0,beta=1, l1_ratio=.5).fit(tfidf)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()

    # print("# : ",tf_vectorizer.vocabulary)
    print_top_words(nmf, tfidf_feature_names, n_top_words)

    lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=50,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=1)
    lda.fit(tfidf)

    asd = get_occurance(reviews)
    #print(asd)
    print("\nTopics in LDA model:")
    tf_feature_names = tf_vectorizer.get_feature_names()
    print_top_words(lda, tfidf_feature_names, n_top_words)

def mean_shift():
    id = "b'CC9ttbNktyxl9tRHkUG30w'"
    reviews = []
    filt = {"_id": id}
    js = shops_collection.find(filter=filt).next()
    for i in range(len(js['reviews'])):
        reviews.append(mli.correctify(js['reviews'][i]['text']))

    tfidf_vectorizer = TfidfVectorizer(max_df=0.5, min_df=2,
                                       max_features=1000,
                                       stop_words='english', ngram_range=(2, 2))
    tfidf = tfidf_vectorizer.fit_transform(reviews)
    mean = ms.MeanShift()

    mean.fit_predict(tfidf)
lda_test()
