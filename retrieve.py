#!/usr/bin/env python
"""
get_top_bottom_movies.py

Usage: get_top_bottom_movies

Return top and bottom 10 movies, by ratings.
"""

import sys

# Import the IMDbPY package.
import imdb




i = imdb.IMDb()
out_encoding = sys.stdout.encoding or sys.getdefaultencoding()

def testIMDB():
    top250 = i.get_top250_movies()
    bottom100 = i.get_bottom100_movies()


    for label, ml in [('top 10', top250[:10]), ('bottom 10', bottom100[:10])]:
        print ''
        print '%s movies' % label
        print 'rating\tvotes\ttitle'
        for movie in ml:
            outl = u'%s\t%s\t%s' % (movie.get('rating'), movie.get('votes'),
                                        movie['long imdb title'])
            print outl.encode(out_encoding, 'replace')

# movie_list is a list of Movie objects, with only attributes like 'title'
# and 'year' defined.
movie_list = i.search_movie('the passion')
# the first movie in the list.
first_match = movie_list[0]
# only basic information like the title will be printed.
print first_match.summary()
# update the information for this movie.
i.update(first_match)
# a lot of information will be printed!
#print first_match.summary()
# retrieve trivia information and print it.
#i.update(first_match, 'trivia')
print("-----DEBUT DE NOTRE PARTIE -------")
def retrieveNmovie(n):

    for movieID in range (30000, 30000+n):

        movie = i.get_movie(str(movieID))
        outl = u'%s\t%s\t%s' % (movie.get('rating'), movie.get('votes'),
                                movie['long imdb title'])
        print outl.encode(out_encoding, 'replace')
        print movie.summary().encode(out_encoding, 'replace')
# Calculer la note en divisant le rating par le nombre de vote ?
retrieveNmovie(10)