#!/usr/bin/python2.7
# -*-coding:Latin-1 -*

from bs4 import BeautifulSoup
import urllib
import json

def getSoupFromUrl(url) :
  html = urllib.urlopen(url).read()
  soup = BeautifulSoup(html, 'html.parser')
  return soup

def findMaxPages(soup):
  max = 0
  for p in soup.find_all("nav", {"class": "pagination cf"}):
    for c in p.find_all("div", {"class": "pagination-item-holder"}):
      max = int(p.find_all("span")[-1].text)
  if (max > 10):
    return 10
  return max

def getReviewsJson(movieUrl) :
  soup = getSoupFromUrl(movieUrl)
  max = findMaxPages(soup)

  json = "\"reviews\":["
  for i in range(max):
    print("Review page ", i + 1)
    url_page = movieUrl + "?page=" + str(i + 1)
    soup_page = getSoupFromUrl(url_page)
    for d in soup_page.find_all("div", {"class": "row item hred"}):
        c = d.find("div", {"class": "col-xs-12 col-sm-9"})
        if c is not None:
          json += "\"" + c.find("p", {"itemprop": "description"}).text.strip().replace('\n', ' ').replace('\r', '').replace('\"', "\\\"") + "\","
  json = json[:-1] + "]"
  return json

def getMovieJson(movieId):
  print("Getting movie id " + movieId)
  url_movie = "http://www.allocine.fr/film/fichefilm_gen_cfilm=" + movieId + ".html"
  soup = getSoupFromUrl(url_movie)
  hash_map = {}
  for j in soup.find_all("div", {"class", "meta-body-item"}):
    key = j.find("span", {"class": "light"}).text.encode("utf-8")
    if key == "Date de sortie":
      hash_map["release"] = j.find_all("span")[-1].text
    elif key == "De" :
      hash_map["author"] = j.find_all("span")[-1].text
    elif key == "Avec" :
      actors = []
      for v in j.find_all("span") :
        actor = v.text
        if actor != " plus " and actor != "Avec":
          actors.append(actor)
      hash_map["actors"] = actors
    elif key == "Genres" :
      genres = []
      for v in j.find_all("span", {"itemprop": "genre"}):
        genres.append(v.text)
      hash_map["genres"] = genres
    elif key == "Nationalité" :
      hash_map["country"] = j.find_all("span")[-1].text.strip()

  url_review = "http://www.allocine.fr/film/fichefilm-" + movieId + "/critiques/spectateurs/"
  soup = getSoupFromUrl(url_review)
  max = findMaxPages(soup)

  reviews = []
  for i in range(max):
    print("Review page ", i + 1)
    url_page = url_review + "?page=" + str(i + 1)
    soup_page = getSoupFromUrl(url_page)
    for d in soup_page.find_all("div", {"class": "row item hred"}):
        c = d.find("div", {"class": "col-xs-12 col-sm-9"})
        if c is not None:
          reviews.append(c.find("p", {"itemprop": "description"}).text.strip().replace('\n', ' ').replace('\r', '').replace('\"', "\\\""))
  hash_map["reviews"] = reviews
  return json.dumps(hash_map)

#json = getMovieJson("207060")
#print(json)

def getMoviesId(soup):
  ids = []
  for a in soup.find_all("a", {"class", "no_underline"}) :
    ids.append(a.get("href")[26:-5])
  return ids

def getBestMoviesId():
  best_movies_url = "http://www.allocine.fr/film/meilleurs/"
  ids = []
  for page in range(10):
    soup = getSoupFromUrl(best_movies_url + "?page=" + str(page + 1))
    ids += getMoviesId(soup)
  return ids

def getData() :
  ids = getBestMoviesId()
  file = open("movies.txt", "w")
  for movieId in ids:
    file.write(getMovieJson(movieId).encode("utf8") + "\n")
  file.close()

print(getMovieJson("144185"))


file = open("lol.txt", "w")
file.write(getMovieJson("144185").encode("utf8") + "\n")
file.close()
