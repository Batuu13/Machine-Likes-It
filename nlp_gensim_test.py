'''
Got most of the code from: https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/
It will be better if we understand what every line of this code does.

gensim LDA document:
https://radimrehurek.com/gensim/models/ldamodel.html
'''
import gensim
from gensim import corpora

import mli_lib as mli
import nlp_gensim_lib as nlpg

reviews = mli.get_reviews_city("Phoenix")
print('Number of reviews:', len(reviews))


doc_clean = [nlpg.clean(doc['text']).split() for doc in reviews]

# Creating the term dictionary of our courpus, where every unique term is assigned an index.
dictionary = corpora.Dictionary(doc_clean)

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=3, id2word = dictionary, passes=50)


