from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
nltk.download('all')
############# OUR PART #############################
from nltk import tokenize
moviesList = []
for line in open('parsed.txt', 'r'):
    moviesList.append(json.loads(line))
sid = SentimentIntensityAnalyzer()

for movie in moviesList:
    print(str(movie['review']))
    if(movie['review']):
        ss = sid.polarity_scores(str(movie['review']))
        for k in sorted(ss):
            print('{0}: {1}, '.format(k, ss[k]), end='')
            print()

