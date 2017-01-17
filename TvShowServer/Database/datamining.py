from api import getShows
from api import getShowsTesting
from sklearn.feature_extraction.text import TfidfVectorizer


weight_seasons = 0.1
weight_episodes = 0.01
weight_year = 0.3
weight_runtime = 0.3
weight_genres = 1.0
weight_actors = 1.0
weight_creators = 1.0
weight_networks = 1.0
weight_status = 0.4
weight_language = 1.0
weight_type = 1.0
weight_votes = 1.0
weight_overview = 1.0
scale_year = 5.0
scale_runtime = 60.0

def getHammingDistance(val1, val2):
    if val1 is None or val2 is None or val1 != val2:
        return 1
    else:
        return 0

def getListDistance(l1, l2):
    max_len = max(len(l1), len(l2))
    commun = 0
    for obj1 in l1:
        val1 = obj1['id']
        for obj2 in l2:
            val2 = obj2['id']
            if getHammingDistance(val1, val2) == 0:
                commun += 1
                break
    return max_len - commun

def getOverviewDistance(overview1,overview2):
    if overview1 is None or overview2 is None:
        return 1 * weight_overview
    corpus = [overview1, overview2]
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(corpus)
    print matrix.toarray()
    return 0

def getGenresDistance(genres1, genres2):
    return getListDistance(genres1, genres2) * weight_genres

def getRuntimeDistance(runtime1, runtime2):
    if runtime1 is None or runtime2 is None:
        return 1 * weight_runtime
    return (abs(runtime2 - runtime1) / scale_runtime) * weight_runtime

def getSeasonsDistance(seasons1, seasons2):
    return abs(seasons2 - seasons1) * weight_seasons

def getEpisodesDistance(episodes1, episodes2):
    return abs(episodes1 - episodes2) * weight_episodes

def getCreatorsDistance(creators1, creators2):
    return getListDistance(creators1, creators2) * weight_creators

def getActorsDistance(actors1, actors2):
    return getListDistance(actors1, actors2) * weight_actors

def getStatusDistance(status1, status2):
    return getHammingDistance(status1, status2) * weight_status

def getTypeDistance(type1, type2):
    return getHammingDistance(type1, type2) * weight_type

def getVotesDistance(votes1, votes2):
    """NULL = 0.0"""
    if votes1 is None or votes2 is None:
        return 1 * weight_votes
    return float(votes1 + votes2) / 2.0

def getYearDistance(date1, date2):
    if date1 is None or date2 is None:
        return 1 * weight_year

    year1 = date1.timetuple().tm_year
    year2 = date2.timetuple().tm_year
    return (abs(year1 - year2) / scale_year) * weight_year

def getLanguageDistance(language1, language2):
    return getHammingDistance(language1, language2) * weight_language

def getNetworksDistance(networks1, networks2):
    return getListDistance(networks1, networks2) * weight_networks

def getDistance(show1, show2):
    return getNetworksDistance(show1['networks'], show2['networks']) + \
           getLanguageDistance(show1['language'], show2['language']) + \
           getYearDistance(show1['airDate'],show2['airDate']) + \
           getVotesDistance(show1['votes'], show2['votes']) + \
           getTypeDistance(show1['type'], show2['type']) + \
           getStatusDistance(show1['status'], show2['status']) + \
           getActorsDistance(show1['actors'], show2['actors']) + \
           getCreatorsDistance(show1['creators'], show2['creators']) + \
           getSeasonsDistance(show1['seasons'], show2['seasons']) + \
           getEpisodesDistance(show1['episodes'], show2['episodes']) + \
           getRuntimeDistance(show1['runtime'], show2['runtime']) + \
           getOverviewDistance(show1['overview'], show2['overview']) + \
           getGenresDistance(show1['genres'], show2['genres'])

def getClusters():
    shows = getShowsTesting()
    """TODO"""

if __name__ == '__main__':
    shows = getShows()
    show1 = shows[0]
    show2 = shows[49]
    print getDistance(show1, show2)
    """FAIRE LES TESTS ICI MAIS LES FONCTIONS SERONT UTILISE DANS LE SERVEUR"""



