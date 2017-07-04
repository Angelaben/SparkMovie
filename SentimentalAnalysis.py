
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
nltk.download('all')

#subjectivity
#The Subjectivity Dataset contains 5000 subjective and 5000 objective processed sentences.
n_feat = 5000
subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')][:n_feat]
obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')][:n_feat]
print(len(subj_docs), len(obj_docs))
#Each document is represented by a tuple (sentence, label). The sentence is tokenized, so it is represented by a list of strings:

#We separately split subjective and objective instances to keep a balanced uniform class distribution in both train and test sets.
percent  =  int((80 * n_feat / 100))
print(percent)
train_subj_docs = subj_docs[:percent]
test_subj_docs = subj_docs[percent:]
train_obj_docs = obj_docs[:percent]
test_obj_docs = obj_docs[percent:]
training_docs = train_subj_docs+train_obj_docs

testing_docs = test_subj_docs+test_obj_docs
sentim_analyzer = SentimentAnalyzer()
# all_words = Return all words tokens from the documents (with duplicates).

# Returns:	A list of all words/tokens in documents.


# nltk.sentiment.util.mark_negation(document, double_neg_flip=False, shallow=False)[source]
# Append  NEG suffix to words that appear in the scope between a negation and a punctuation mark.

all_words_neg = sentim_analyzer.all_words([mark_negation(doc) for doc in training_docs])
#We use simple unigram word features, handling negation:

#unigram word feats : Return most common top n word features.

#Parameters:
#words  a list of words/tokens.
#top n  number of best words/tokens to use, sorted by frequency.

#Returns:
#A list of top n words/tokens (with no duplicates) sorted by frequency.
unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)

# Add a new function to extract features from a document. This function will be used in

# extract unigram feats : Populate a dictionary of unigram features, reflecting the presence/absence in
# the document of each of the tokens in unigrams.
sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)
#We apply features to obtain a feature value representation of our datasets:

training_set = sentim_analyzer.apply_features(training_docs)
test_set = sentim_analyzer.apply_features(testing_docs)
#We can now train our classifier on the training set, and subsequently output the evaluation results:

trainer = NaiveBayesClassifier.train

classifier = sentim_analyzer.train(trainer, training_set)
#Training classifier
for key,value in sorted(sentim_analyzer.evaluate(test_set).items()):
     print('{0}: {1}'.format(key, value))
############### OUR PART #############################
from nltk import tokenize
lines_list = tokenize.sent_tokenize(paragraph)
sentences.extend(lines_list)