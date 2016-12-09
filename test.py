import csv
import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client['ml']
shops_collection = db.get_collection("shops")

# Add Businesses


def insert_business():
    with open('yelp_academic_dataset_business.csv') as csvfile:
        reader_bus = csv.DictReader(csvfile)

        for row_bus in reader_bus:
            doc = {
                "business_id": row_bus['business_id'],
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
            filt = {"business_id": row_rev['business_id']}
            upd = {
                '$push' : {
                    'reviews' : doc
                }
            }
            shops_collection.find_one_and_update(filter=filt,update=upd)


insert_review()
