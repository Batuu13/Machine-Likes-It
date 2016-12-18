# Machine-Likes-It

For the dataset, you need to extract twice. Just add another ".tar" to the "yelp_dataset" file and extract again.

json_to_csv_converter.py is for converting json to csv

mli_lib is our library

test.py is for reading from csv file and write it into mongoDB.

review_and_business_join_to_csv.py takes the csv of reviews and businesses, adds 'name', 'state' and 'city' to all reviews and writes the reviews to a .csv file.

**To import data to MongoDB, execute the following command:**
mongoimport --db yelpdata --collection reviews --type csv --file reviews.csv --headerline

(you may need to add MongoDB bin folder to your path, or you should execute this command at that folder)



