
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
allocine = True
##################### PARTIE PARSING DE DONNEE ET TRAITEMENT  : TMDB    #############################
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



##################### PARTIE PARSING DE DONNEE ET TRAITEMENT  : ALLOCINE  #############################
import urllib3
import json
from threading import Thread, RLock
from bs4 import BeautifulSoup

PAGE_LIMIT = 2 # Nombre de review max
lock = RLock()

def getParsedHTML(url, decode = 'latin-1'):
    http_pool = urllib3.connection_from_url(url)
    r = http_pool.urlopen('GET', url)
    parsedHTML = BeautifulSoup(r.data.decode(decode), "html5lib")
    return parsedHTML

def loadURLs():
    file = open("urls.txt", 'r')
    urls = file.readlines()
    file.close()
    for i in range(len(urls)):
        urls[i] = urls[i][:-1]
    return urls

def critique_press_url(movie_id):
    return "http://www.allocine.fr/film/fichefilm-" + movie_id + "/critiques/presse/"
def critique_spectateurs_url(movie_id):
    return "http://www.allocine.fr/film/fichefilm-" + movie_id + "/critiques/spectateurs/"

class MoviesURLSGetter(Thread):
    def __init__(self, indexes, defaultURL):
        Thread.__init__(self)
        self.indexes = indexes
        self.defaultURL = defaultURL

    def run(self):
        self.links = []
        i = 0
        for page in self.indexes:
            i += 1
            url = self.defaultURL + "?page=" + str(page)
            html = getParsedHTML(url)
            self.links += ["http://www.allocine.fr" + b['href'] for b in html.body.find_all('a', {'class': 'meta-title-link'})]
            print(i, len(self.indexes))


def getMoviesUrls():
    defaultURL = "http://www.allocine.fr/films/alphabetique/"
    defaultHtml = getParsedHTML(defaultURL)
    pages_num = int(defaultHtml.body.find('nav', {'class': 'pagination cf'}).find_all('span')[-1].get_text(' ', strip=True))
    threads = []
    nb_threads = 10
    pages_per_thread = pages_num // nb_threads - 1
    for i in range(nb_threads - 1):
        threads.append(MoviesURLSGetter(range(pages_per_thread * i, pages_per_thread * (i + 1)), defaultURL))
    threads.append(MoviesURLSGetter(range(pages_per_thread * (nb_threads - 1), pages_num), defaultURL))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    links = []
    file = open('urls.txt', 'w')
    for thread in threads:
        for link in thread.links:
            file.write(link + '\n')
            links.append(link)

    file.close()

def getPressCommentsFromPage(url):
    html = getParsedHTML(url, decode='utf-8')
    press_names = [b.span.text for b in html.body.find_all('h2', {'class': 'title'}) ]
    comments = [b.text.split('\n')[1].split('            ')[1].replace('\u2009', ' ') for b in html.body.find_all('p', {'class': 'text'})]
    dic = {}
    for i in range(len(press_names)):
        dic[press_names[i]] = comments[i]
    return dic

def getSpectateursCommentsFromPage(url):
    global PAGE_LIMIT
    url_of_page = url
    comments_per_page = 15
    current_page = 1
    html = getParsedHTML(url_of_page, decode='utf-8')
    reviews_count = int(html.find('span', {'itemprop': 'reviewCount'}).text)
    pages_count = reviews_count // comments_per_page + (1 if reviews_count % comments_per_page > 0 else 0)
    limit = min(pages_count, PAGE_LIMIT if PAGE_LIMIT != None else pages_count)
    reviews = []
    while current_page <= limit:
        reviews += [b.get_text().replace("Spoiler:  ", "").replace('\n', ' ').replace('                                                                  ', '').replace('  ', ' ') for b in html.find_all('p', {'itemprop': 'description'})]
        current_page += 1
        if (current_page <= limit):
            url_of_page = url + "?page=" + str(current_page)
            html = getParsedHTML(url_of_page, decode='utf-8')
    return reviews

def getDataFromMoviePage(url):
    html = getParsedHTML(url, decode="utf-8")
    movie_id = url.split("=")[1].split(".html")[0]
    infos = html.head.title.get_text(' ', strip=True).split(' - ')
    movie_title = infos[0]
    movie_date = infos[1].split(' ')[-1] if len(infos) > 2 else ""
    movie_director = html.head.find('meta', {'property' : 'video:director'})['content']
    disable_buttons = [b.div.get_text(' ', strip=True) for b in html.body.find_all('span', {'class': 'item js-item-mq inactive'})]
    reviews_press_enable = 'Critiques presse' not in disable_buttons
    reviews_people_enable = 'Critiques spectateurs' not in disable_buttons
  #  press_reviews = None if not reviews_press_enable else getPressCommentsFromPage(critique_press_url(movie_id))
    spectators_reviews = None if not reviews_people_enable else getSpectateursCommentsFromPage(critique_spectateurs_url(movie_id))

    json_dic = {'id': movie_id,
                'title': movie_title,
                'date': movie_date,
                'director': movie_director,
      #          'press_reviews': press_reviews,
                'spectators_reviews': spectators_reviews
                }

    return json_dic


class ThreadedRequest(Thread):
    def __init__(self, urls, outfile):
        Thread.__init__(self)
        self.urls = urls
        self.outfile = outfile

    def run(self):
        i = 1
        for url in self.urls:
            dic = getDataFromMoviePage(url)
            with lock:
                json.dump(dic, self.outfile, ensure_ascii=False)
                self.outfile.write('\n')
                print(i)
                i += 1


def getAllocineInMovies():
    urls = loadURLs()[:1000]
    outfile = open('movies.json', 'w')
    threads = [ThreadedRequest(urls[(i * 100):(i + 1) * 100], outfile) for i in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
##################### RETRIEVE DATA ############################################

if importer :
    if allocine :
        getAllocineInMovies()
    else:
        retrieveData(100, "parsed.txt")
    import json
from pprint import pprint
moviesList = []

if allocine :
    for line in open('movies.json', 'r'):
        print("ALLOCINE CALLED ")
        moviesList.append(json.loads(line))
else : # TMDB
    for line in open('parsed.txt', 'r'):
        moviesList.append(json.loads(line))
##################### PARTIE KAFKA ###############################################
produced = False
consumed  = False
class Producer(threading.Thread):
    daemon = True

    def run(self):
        print("Producer begin") # IP CLara
        producer = KafkaProducer(bootstrap_servers='localhost:9092')

        for data in moviesList :
            if(debug):
                print("data to send ",data)
            producer.send("my-topic", json.dumps(data))
        print("Data produced")
        produced = True
        producer.flush()
        producer.close()
          #  producer.close()
class Consumer(multiprocessing.Process):
    daemon = True

    def __init__(self, id):
        self.ID = id
    def run(self):

        print("Consumer begin ",self.ID) # IP CLara
        #consumer = KafkaConsumer(bootstrap_servers='localhost:9092',

        consumer = KafkaConsumer(bootstrap_servers = '37.163.95.205',
                                  group_id='StarPlatinium',
                                 auto_offset_reset='earliest', consumer_timeout_ms = 100 )
        consumer.subscribe(['my-topic'])
        self.retrievedData = []
        self.nb_elements = 0

        for message in consumer:
            try :

                msg = json.loads(message.value)
                self.retrievedData.append(msg)
                if debug:
                    print("Title received : ", msg['title'], " with id ",self.ID)
                self.nb_elements += 1
            except Exception as err:
                print("Error ", err)
        print("Consuming done : ",self.nb_elements, " elements")
        consumer.unsubscribe()
        consumer.close()

class Analyzer(multiprocessing.Process):
    daemon = True

    def run(self):

        Myanalyzer = SentimentalAnalysis

        print("Analyzer begin")
#        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092','37.163.95.205',
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
        producer = KafkaProducer(bootstrap_servers='localhost:9092')


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
    Producer(),
    Consumer(1),
    Consumer(2),
    Analyzer()
]
######################## MAIN PART ############################
for t in tasks :
    t.run()
#Producer().run()
#Consumer().run()
#Analyzer().run()



logging.basicConfig(
        format='%(name)s:%(thread)d:%(process)d:%(message)s',
        level=logging.INFO)


print("End")
