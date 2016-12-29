'''
Got most of the code from: https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/
It will be better if we understand what every line of this code does.
'''

'''
One must download nltk data first to use these. In order to do so type these in any Python console:
import nltk
nltk.download()
A new window will open. In that windows select the required packages(I don't know yet) or download all packages.
'''

'''
gensim LDA document:
https://radimrehurek.com/gensim/models/ldamodel.html
'''

from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string

import gensim
from gensim import corpora

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()


def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


#cleans the reviews, does the lda, prints results to console and appends them 'tests.txt' file.
def do_lda(reviews, parameters):

    doc_clean = [clean(doc['text']).split() for doc in reviews]

    # Creating the term dictionary of our courpus, where every unique term is assigned an index.
    dictionary = corpora.Dictionary(doc_clean)

    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

    # Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel

    # Running and Trainign LDA model on the document term matrix.

    ldamodel = Lda(doc_term_matrix, num_topics=parameters.get('num_topics'), id2word=dictionary,
                   passes=parameters.get('passes'), alpha=parameters.get('alpha'), eta=parameters.get('eta'))

    result = ldamodel.print_topics(num_topics=parameters.get('print_num_topic'), num_words=parameters.get('print_num_word'))

    print(result)

    toWrite = '\n\nParameters \n' + str(parameters) + '\nResult \n' + str(result)
    with open("tests.txt", "a") as testfile:
        testfile.write(toWrite)
