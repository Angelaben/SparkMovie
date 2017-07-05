from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
nltk.download('all')
############# OUR PART #############################
from nltk import tokenize

def loader():
    moviesList = []
    for line in open('parsed.txt', 'r'):
        moviesList.append(json.loads(line))
    return moviesList
def sentimentAnalysis(moviesList):
    sid = SentimentIntensityAnalyzer()
    returnList = []
    for review in moviesList:

        if(review):
            print("Movie analyzer : ", review)
            ss = sid.polarity_scores(str(review))
            print("SS : ",ss['compound'])
           # for k in sorted(ss):
            #    print('{0}: {1}, '.format(k, ss[k]))#, end='')

            returnList.append(ss['compound'])
        else:
            returnList.append([])
    return returnList
def analysis(review):
    sid = SentimentIntensityAnalyzer()
    returnList = []
    if (review):
        print("Movie analyzer : ", review)
        ss = sid.polarity_scores(str(review))
        print("SS : ", ss['compound'])

        returnList.append(ss['compound'])
    else:
        returnList.append([])
    return returnList
