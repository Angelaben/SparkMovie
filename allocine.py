import urllib3
import json
from threading import Thread, RLock
from bs4 import BeautifulSoup

PAGE_LIMIT = 2
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
    print(pages_num)
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
              #  'press_reviews': press_reviews,
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
                json.dump(dic, outfile, ensure_ascii=False)
                outfile.write('\n')
                print(i)
                i += 1



# getMoviesUrls()
urls = loadURLs()[:1000]
outfile = open('movies.json', 'w')
threads = [ThreadedRequest(urls[(i * 100):(i + 1) * 100], outfile) for i in range(10)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

