from api import *
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.cluster import KMeans
from sklearn import metrics
import numpy as np

class Engine(object):
    shows = None
    dataframe = None
    tfidf_vector = None
    tfidf_matrix = None

    def start_engine(self):
        print('starting engine')
        self.shows = getShows()
        self.dataframe = pd.DataFrame(self.shows)
        self.tfidf_vector = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
        l = list()
        for i in range(len(self.shows)):
            l.append(self.dataframe[1][i] + " " + self.dataframe[3][i])
        data = np.array(l)
        self.tfidf_matrix = self.tfidf_vector.fit_transform(data)
        print('engine ready')

def findSimilarShows(engine, show_index):
    n = 10
    cosine_similarities = \
        linear_kernel(engine.tfidf_matrix[show_index], engine.tfidf_matrix).flatten()
    indices = [i for i in cosine_similarities.argsort()[-n:] if i != show_index]
    similar_shows = list()
    for i in indices[0:n]:
        show = getShowByID(str(i))
        similar_shows.append(show)
    return similar_shows

def findSuggestionsFromContent(user_id, engine):
    shows = getUserLikeShows(str(user_id))

    list_ids = list()
    for show in shows:
        list_ids.append(show['id'])

    dataframe = pd.DataFrame(shows)
    tfidf_vector = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    tfidf_matrix = tfidf_vector.fit_transform(dataframe['overview'])

    best_k = 1
    MAX = len(shows) / 2
    best_score = -1

    for k in range(2, MAX + 1):
        model = KMeans(k).fit(tfidf_matrix)

        scores = metrics.silhouette_samples(tfidf_matrix, model.labels_)
        negative_scores_count = len([x for x in scores if x < 0])
        model_score = negative_scores_count / float(len(scores))

        if model_score > best_score:
            best_score = model_score
            best_k = k

    clusters = KMeans(best_k).fit(tfidf_matrix)

    list_tfidf = list()
    for k in range(best_k):
        i = 0
        tfidf_sum = 0.0
        divide = 0.0
        for indice in clusters.labels_.tolist():
            if k == indice:
                tfidf_sum += engine.tfidf_matrix[shows[i]['id']]
                divide += 1.0
            i += 1
        tfidf = tfidf_sum / divide
        list_tfidf.append(tfidf)

    n = 50
    similar_shows = list()
    for tfidf in list_tfidf:
        cosine_similarities = linear_kernel(tfidf, engine.tfidf_matrix).flatten()
        indices = [i for i in cosine_similarities.argsort()[-n:]]
        for i in indices[0:n]:
            if i not in list_ids:
                show = getShowByID(str(i))
                similar_shows.append(show)

    return similar_shows[0:10]

def findSuggestionsFromUsers(user_id):
    shows_liked = getShowsLiked()
    users_ids = getUsersId()
    shows_not_liked = getShowOthersLiked(user_id)

    matrix = list()
    for user in users_ids:
        user_row = list()
        user_shows = getUsersShowsId(user)
        for id in shows_liked:
            if(id in user_shows):
                user_row.append(1)
            else:
                user_row.append(0)
        matrix.append(user_row)

    E = np.array(matrix)
    C = np.corrcoef(E)
    shows = list()
    for id_show in shows_not_liked:
        index = shows_liked.index(id_show)
        score = 0.0
        for id_user in users_ids:
            if id_user == user_id:
                continue
            score += C[int(id_user)-1][int(user_id)-1] * E[int(id_user)-1][index]
        if score > 0:
            show = getShowByID(str(id_show))
            shows.append(show)

    return shows[0:10]