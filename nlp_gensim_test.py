import mli_lib as mli
import nlp_gensim_lib as nlpgen

parameters = {
    'pos_or_neg': 'pos',
    'sample_size': 5000,
    'num_topics': 3,
    'passes': 10,
    #some possible values are 'auto' and 'symmetric'
    'alpha': 'symmetric',
    'print_num_topic': 3,
    'print_num_word': 3,
    #some possible values are a scalar or None or 'auto'
    'eta': 'auto',
}

reviews = mli.get_reviews_city("Phoenix", parameters.get('pos_or_neg'))[0:parameters.get('sample_size')]
print('Number of reviews:', len(reviews))

nlpgen.do_lda(reviews, parameters)





