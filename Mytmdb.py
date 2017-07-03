import tmdbsimple as tmdb
tmdb.API_KEY = '913158e2a391c2720b155fdbe7cddce5'

def retrieveData(n, path):
    fichier = open(path, "w")
    cpt = 0
    for i in range(1000000):
        if (cpt == n):
            return
        try :
            res = tmdb.Movies(i)
            movie = res.info()
            print(movie)
            fichier.write(movie)
            fichier.write("\n")
            cpt += 1
        except Exception:
            print("not found ")
    fichier.close()

retrieveData(2000, "parsed.txt")