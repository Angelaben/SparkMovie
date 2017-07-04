
#!/usr/bin/env python
import tmdbsimple as tmdb
tmdb.API_KEY = '913158e2a391c2720b155fdbe7cddce5'
import json
import threading, logging, time
import multiprocessing

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from kafka import KafkaConsumer, KafkaProducer

debug = False
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
                #print(elements['content'])
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
        producer = KafkaProducer(bootstrap_servers='localhost:9092')

        for data in moviesList :
            producer.send("my-topic", json.dumps(data))
        print("Data produced")
class Consumer(multiprocessing.Process):
    daemon = True

    def run(self):

        print("Consumer begin")
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                 auto_offset_reset='earliest') # Trouverl a definition
        consumer.subscribe(['my-topic'])
        self.retrievedData = []
        self.nb_elements = 0
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

    def consume(self):
        iteration = 0
        sentim_analyzer = SentimentAnalyzer()
        tok_stop = len(self.retrievedData)
        print("Size ",tok_stop)
        training_set = self.retrievedData[:tok_stop - self.nb_elements : -1] # Parcourir liste en sens inverse sur
        # Un certains nombre d'elements car pour l'instant probleme pour vider brokers
        all_words_neg = sentim_analyzer.all_words([mark_negation(doc) for doc in training_set])

        for elem in self.retrievedData[::-1]:
            if iteration == self.nb_elements :
                break # Gerer ce cas tant que j'ai pas trouve comment vider un brokers
            iteration += 1

######################## MAIN PART ############################

tasks = [
        Producer(),
        Consumer()
]
from pprint import pprint

import json

moviesList = []
for line in open('parsed.txt', 'r'):
    moviesList.append(json.loads(line))

for t in tasks:
    t.start()

#time.sleep(10)

logging.basicConfig(
        format='%(name)s:%(thread)d:%(process)d:%(message)s',
        level=logging.INFO)
