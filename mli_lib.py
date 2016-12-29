import pymongo
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

review_col_name = 'reviews'
db_name = 'yelpdata'

def correctify(string):
    ''' #Example string : b'test123' , returns test123
    :param string: Desired raw string
    :return: Valid string
    '''
    return string[2:-1]

def get_business_id_list(reviewCount):
    client = pymongo.MongoClient('localhost', 27017)
    db = client[db_name]
    review_col = db.get_collection(review_col_name)

    return review_col.aggregate([
        {
            "$group": {
                "_id": "$business_id",
                "count": { "$sum": 1}
            }
        },
        {
            "$match": {
                "count": {"$gte": reviewCount}
            }
        }
    ])

def get_current_states():
    client = pymongo.MongoClient('localhost', 27017)
    db = client[db_name]
    review_col = db.get_collection(review_col_name)
    return review_col.distinct("state")

def get_current_cities():
    client = pymongo.MongoClient('localhost', 27017)
    db = client[db_name]
    review_col = db.get_collection(review_col_name)
    return review_col.distinct("city")


def get_reviews_state(state):
    client = pymongo.MongoClient('localhost', 27017)
    db = client[db_name]
    review_col = db.get_collection(review_col_name)
    state_filter = {
        "state": state
    }
    reviews = review_col.find(filter=state_filter)
    s_list = []
    for rev in reviews:
        s_list.append(rev)
    return s_list


def get_reviews_business(business_id, type = "all"):
    client = pymongo.MongoClient('localhost', 27017)
    db = client[db_name]
    review_col = db.get_collection(review_col_name)
    if type == "pos":
        star = {"$gt": 3}
    elif type == "neg":
        star = {"$lt": 3}
    else:
        star = {"$gt": 0}
    business_filter = {
        "business_id": business_id,
        "stars": star
    }
    reviews = review_col.find(filter=business_filter)
    b_list = []
    for rev in reviews:
        b_list.append(rev)
    return b_list

def get_reviews_city(city, type = "all"):


    client = pymongo.MongoClient('localhost', 27017)
    db = client[db_name]
    review_col = db.get_collection(review_col_name)
    if type == "pos":
        star = { "$gt": 3 }
    elif type == "neg":
        star = { "$lt": 3 }
    else:
        star = { "$gt": 0 }
    city_filter = {
        "city": city,
        "stars": star
    }
    reviews = review_col.find(filter = city_filter)
    c_list = []
    for city in reviews:
        c_list.append(city)
    return c_list

def split_sentence(reviews):
    new_rew = []
    for i in range(len(reviews)):
        splitted = str(correctify(reviews[i]['text'])).split(".")
        for sent in splitted:
            new_rew.append(sent)
    return new_rew

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" | ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))
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

def do_nmf(rev,n_features = 1000 ,n_topics = 10,n_top_words = 5,isSplit = 1,maxdf = 0.5,mindf = 0.0,range=(2,2)):
    if isSplit == 1:
        rev = split_sentence(rev)
    else:
        rev = [review['text'] for review in rev]
    # Dictionary
    tfidf_vectorizer = TfidfVectorizer(max_df=maxdf,min_df= mindf,
                                       max_features=n_features,
                                       stop_words='english', ngram_range=range)
    tfidf = tfidf_vectorizer.fit_transform(rev)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    ##
    nmf = NMF(n_components=n_topics, random_state=1,
              alpha=0.0, beta=1, l1_ratio=.5).fit(tfidf)
    print_top_words(nmf, tfidf_feature_names, n_top_words)


def do_lda(rev,n_features = 1000 ,n_topics = 6,n_top_words = 6,isSplit = 1,maxdf = 0.5,mindf = 0.0,range=(2,2)):
    if isSplit == 1:
        rev = split_sentence(rev)
    else:
        rev = [review['text'] for review in rev]

    tfidf_vectorizer = TfidfVectorizer(max_df=maxdf,min_df= mindf,
                                       max_features=n_features,
                                       stop_words='english',ngram_range=range)
    tfidf = tfidf_vectorizer.fit_transform(rev)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=1)
    lda.fit(tfidf)
    print([tfidf_feature_names[i] for i in lda.components_[0].argsort()[:-n_top_words - 1:-1]])
    print(lda.components_[0])
    print("\nTopics in LDA model:")
    print_top_words(lda, tfidf_feature_names, n_top_words)


