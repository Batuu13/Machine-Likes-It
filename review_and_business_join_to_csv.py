import csv

def correctify(string):
    ''' #Example string : b'test123' , returns test123
    :param string: Desired raw string
    :return: Valid string
    '''
    return string[2:-1]

business_arr = []
with open('yelp_academic_dataset_business.csv') as csvfile:
    business = csv.DictReader(csvfile)

    for row_bus in business:
        doc = {
            "business_id": correctify(row_bus['business_id']),
            "name": correctify(row_bus['name']),
            "state": correctify(row_bus['state']),
            "city": correctify(row_bus['city'])
        }
        business_arr.append(doc)

review_arr = []
with open('yelp_academic_dataset_review.csv') as csvfile:
    review = csv.DictReader(csvfile)

    for row_rev in review:
        doc = {
            "business_id": correctify(row_rev['business_id']),
            "state": "",
            "city": "",
            "stars": row_rev['stars'],
            "text": correctify(row_rev['text'])
        }
        review_arr.append(doc)



#define the size of review_arr again, too much entry needs too much time.
sample_size = 500000
review_arr = review_arr[0:sample_size]

for i in range(len(review_arr)):
    bus = next(item for item in business_arr if item['business_id'] == review_arr[i]['business_id'])
    review_arr[i]['city'] = bus['city']
    review_arr[i]['state'] = bus['state']
    review_arr[i]['name'] = bus['name']

keys = review_arr[0].keys()
with open('reviews.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(review_arr)
