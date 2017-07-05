
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

debug = True
importer = False
##################### PARTIE PARSING DE DONNEE ET TRAITEMENT #############################
def retrieveData(n, path):
    fichier = open(path, "w")
    cpt = 0
    for i in range(1000000):
        if (cpt == n):
            return
        try :
            res = tmdb.Movies(i)
            movie = res.info()
            reviews = res.reviews()
            listComment = []
            for elements in reviews['results']:
                print(elements['content'])
                listComment.append(elements['content'])

            movie["review"] = listComment

            jsonarray = json.dumps(movie)
            fichier.write(jsonarray)
            fichier.write("\n")
            cpt += 1

        except Exception as err:
            print("not found ", err)
    fichier.close()

if importer :
    retrieveData(100, "parsed.txt")


##################### PARTIE KAFKA ###############################################
class Producer(threading.Thread):
    daemon = True

    def run(self):
        print("Producer begin")
        producer = KafkaProducer(bootstrap_servers='localhost:9092')

        for data in moviesList :
            if(debug):
                print("data to send ",data)
            producer.send("my-topic", json.dumps(data))
        print("Data produced")
      #  producer.close()
class Consumer(multiprocessing.Process):
    daemon = True

    def run(self):

        print("Consumer begin")
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                 auto_offset_reset='earliest', consumer_timeout_ms=1000)
        consumer.subscribe(['my-topic'])
        self.retrievedData = []
        self.nb_elements = 0
        print(consumer)
        for message in consumer:
            try :

                msg = json.loads(message.value)
                self.retrievedData.append(msg)
                if debug:
                    print("Title received :  %s" % (msg['title']))
                self.nb_elements += 1
            except Exception as err:
                print("Error ", err)
        print("Consuming done : ",self.nb_elements, " elements")
       # consumer.unsubscribe()

class Analyzer(multiprocessing.Process):
    daemon = True

    def run(self):
        Myanalyzer = SentimentalAnalysis

        print("Analyzer begin")
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                     auto_offset_reset='earliest', consumer_timeout_ms=1000)
        consumer.subscribe(['my-topic'])
        print("Subscription analyzer: OK")
        moviesList = []
        for message in consumer:
            jsoned =  json.loads(message.value)
            #moviesList.append(jsoned['review'])
            note = Myanalyzer.analysis(jsoned['review'])
            if (note):
                jsoned['ownRating'] = note
            else :
                jsoned['ownRating'] = 0
            moviesList.append(jsoned)
        consumer.unsubscribe()
        producer = KafkaProducer(bootstrap_servers='localhost:9092')

        for data in moviesList:
            if (debug):
                print("dataAnalyzer to send ", data)
            producer.send("my-topic", json.dumps(data))
        print("DataAnalyse produced")
      #  producer.close()

######################## MAIN PART ############################

tasks = [
        Producer(),
        Consumer(),
        Analyzer()
]
from pprint import pprint

import json

moviesList = []
for line in open('parsed.txt', 'r'):
    moviesList.append(json.loads(line))

for t in tasks:
    t.start()
    time.sleep(1) # Synchro que producer soit avant
# Set le server properties a true pour le delete, puis lancer la ligne pour vider
#time.sleep(10)

logging.basicConfig(
        format='%(name)s:%(thread)d:%(process)d:%(message)s',
        level=logging.INFO)

time.sleep(15)
print("Testeur d'analyseur :")
print("Consumer begin")
consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                         auto_offset_reset='earliest', consumer_timeout_ms=1000)
consumer.subscribe(['my-topic'])
for message in consumer:
    try:

        msg = json.loads(message.value)
        if debug:
            print("rating obtained :  %s" % (msg['ownRating']))

    except Exception as err:
        print("Error ", err)