
#!/usr/bin/env python
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
import tmdbsimple as tmdb
tmdb.API_KEY = '913158e2a391c2720b155fdbe7cddce5'
import json
import threading, logging, time
import multiprocessing
import SentimentalAnalysis
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from kafka import KafkaConsumer, KafkaProducer
class Consumer(multiprocessing.Process):
    daemon = True

    def __init__(self, id):
        self.ID = id
    def run(self):

        print("Consumer begin ",self.ID) # IP CLara
        consumer = KafkaConsumer(bootstrap_servers='172.20.10.4:9092',
                                 group_id='StarPlatinium',
                                 auto_offset_reset='earliest', consumer_timeout_ms = 100 )
        consumer.subscribe(['my-topic'])
        self.retrievedData = []
        self.nb_elements = 0

        for message in consumer:
            try :

                msg = json.loads(message.value)
                self.retrievedData.append(msg)
                print("Title received : ", msg['title'], " with id ",self.ID)
                self.nb_elements += 1
            except Exception as err:
                print("Error ", err)
        print("Consuming done : ",self.nb_elements, " elements")
        consumer.unsubscribe()
        consumer.close()

allocine = True
debug = True
class Analyzer(multiprocessing.Process):
    daemon = True

    def run(self):

        Myanalyzer = SentimentalAnalysis

        print("Analyzer begin")
#        consumer = KafkaConsumer(bootstrap_servers='172.20.10.4:9092',
        consumer = KafkaConsumer(bootstrap_servers='172.20.10.4',
                                     auto_offset_reset='earliest', consumer_timeout_ms=10000)
        consumer.subscribe(['my-topic'])
        print("Subscription analyzer: OK")
        moviesList = []
        for message in consumer:
            if allocine :
                jsoned = json.loads(message.value)
                #note = Myanalyzer.analysis(jsoned['spectators_reviews'])

                from textblob import TextBlob
                from textblob_fr import PatternTagger, PatternAnalyzer
                print(jsoned)
                if (jsoned['spectators_reviews']):
                    note = 0
                    nbNote = 1
                    for elem in jsoned['spectators_reviews']:
                        blob = TextBlob(elem, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
                        note += blob.sentiment[0]
                        nbNote += 1
                    note /= nbNote
                 #   print("Note obtenu ", note)
                    jsoned['ownRating'] = note
                    moviesList.append(jsoned)
            else :
                jsoned =  json.loads(message.value)
                #moviesList.append(jsoned['review'])
                note = Myanalyzer.analysis(jsoned['review'])

                if (note):
                    jsoned['ownRating'] = note
                else :
                    jsoned['ownRating'] = 0
                moviesList.append(jsoned)
        producer = KafkaProducer(bootstrap_servers='172.20.10.4:9092')


        for data in moviesList:
            if (debug):
                print("dataAnalyzer to send ", data)
                data['spectators_reviews'] = "" # Supprime les reviews pour pas s'embeter
                producer.send("my-ratings", json.dumps(data))
            print("Sent")
        producer.flush()
        producer.close()
        print("DataAnalyse produced")


tasks = [
    Consumer(1),
    Consumer(2),
]
for t in tasks :
    t.run()
logging.basicConfig(
        format='%(name)s:%(thread)d:%(process)d:%(message)s',
        level=logging.INFO)


print("End")
