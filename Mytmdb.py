
import tmdbsimple as tmdb
tmdb.API_KEY = '913158e2a391c2720b155fdbe7cddce5'
import json
#!/usr/bin/env python
import threading, logging, time
import multiprocessing

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
        retrievedData = []
        for message in consumer:
            try :

                msg = json.loads(message.value)
                retrievedData.append(msg)
                print("Title received :  %s" % (msg['title']))
            except Exception as err:
                print("Error ", err)




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
