from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
nltk.download('all')

#subjectivity
#The Subjectivity Dataset contains 5000 subjective and 5000 objective processed sentences.
n_feat = 100 #5000
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
moviesList = []
for line in open('parsed.txt', 'r'):
    moviesList.append(json.loads(line))


def Mytokenize(moviesList):
    lines_list = []
    for line in moviesList:
        st = str(line['review'])
        print("Str ",st)
        if (line['review']):
            lines_list.append(st.split(" "))
    print(lines_list)
    return lines_list
appended = ""
sid = SentimentIntensityAnalyzer()


for movie in moviesList:
    print(str(movie['review']))
    if(movie['review']):
        ss = sid.polarity_scores(str(movie['review']))
        for k in sorted(ss):
            print('{0}: {1}, '.format(k, ss[k]), end='')
            print()


lines_list = tokenize.sent_tokenize(appended)
tricky_sentences = [
    "Most automated sentiment analysis tools are shit.",
    "VADER sentiment analysis is the shit.",
    "Sentiment analysis has never been good.",
    "Sentiment analysis with VADER has never been this good.",
    "Warren Beatty has never been so entertaining.",
    "I won't say that the movie is astounding and I wouldn't claim that \
    the movie is too banal either.",
    "I like to hate Michael Bay films, but I couldn't fault this one",
    "It's one thing to watch an Uwe Boll film, but another thing entirely \
    to pay for it",
    "The movie was too good",
    "This movie was actually neither that funny, nor super witty.",
    "This movie doesn't care about cleverness, wit or any other kind of \
    intelligent humor.",
    "Those who find ugly meanings in beautiful things are corrupt without \
    being charming.",
    "There are slow and repetitive parts, BUT it has just enough spice to \
    keep it interesting.",
    "The script is not fantastic, but the acting is decent and the cinematography \
    is EXCELLENT!",
    "Roger Dodger is one of the most compelling variations on this theme.",
    "Roger Dodger is one of the least compelling variations on this theme.",
    "Roger Dodger is at least compelling as a variation on the theme.",
    "they fall in love with the product",
    "but then it breaks",
    "usually around the time the 90 day warranty expires",
    "the twin towers collapsed today",
    "However, Mr. Carter solemnly argues, his client carried out the kidnapping \
    under orders and in the ''least offensive way possible.''"
 ]
sentences = ["VADER is smart, handsome, and funny.", # positive sentence example
    "VADER is smart, handsome, and funny!", # punctuation emphasis handled correctly (sentiment intensity adjusted)
    "VADER is very smart, handsome, and funny.",  # booster words handled correctly (sentiment intensity adjusted)
    "VADER is VERY SMART, handsome, and FUNNY.",  # emphasis for ALLCAPS handled
    "VADER is VERY SMART, handsome, and FUNNY!!!",# combination of signals - VADER appropriately adjusts intensity
    "VADER is VERY SMART, really handsome, and INCREDIBLY FUNNY!!!",# booster words & punctuation make this close to ceiling for score
    "The book was good.",         # positive sentence
    "The book was kind of good.", # qualified positive sentence is handled correctly (intensity adjusted)
    "The plot was good, but the characters are uncompelling and the dialog is not great.", # mixed negation sentence
    "A really bad, horrible book.",       # negative sentence with booster words
    "At least it isn't a horrible book.", # negated negative sentence with contraction
    ":) and :D",     # emoticons handled
    "",              # an empty string is correctly handled
    "Today sux",     #  negative slang handled
    "Today sux!",    #  negative slang with punctuation emphasis handled
    "Today SUX!",    #  negative slang with capitalization emphasis
    "Today kinda sux! But I'll get by, lol" # mixed sentiment example with slang and constrastive conjunction "but"
 ]
#sentences.extend(tricky_sentences)
#sid = SentimentIntensityAnalyzer()
##for sentence in #sentences:
 #   print(sentence)
 #   ss = sid.polarity_scores(sentence)
 #   for k in sorted(ss):
 #       print('{0}: {1}, '.format(k, ss[k]), end='')
 #   print()
#appended.extend(lines_list)