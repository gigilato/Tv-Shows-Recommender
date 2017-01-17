from TvShowServer.Model.creator import *
from TvShowServer.Model.genre import *
from TvShowServer.Model.network import *
from TvShowServer.Model.actor import *
from TvShowServer.Model.user import *
from TvShowServer.Model.show import *
from psycopg2 import *

# noinspection SqlResolve
def getHomeShows():
    connection = connect(user=db_user, host=db_host, password=db_password, database=db_name)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM shows WHERE poster IS NOT NULL LIMIT 10')
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    shows = list()
    for data in rows:
        show = Show(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],
                    data[10],data[11],data[12], data[13])
        shows.append(show.serialize())
    return shows

# noinspection SqlResolve
def getHomeUserLikeShows(id_user):
    genre = '\'' + id_user + '\''
    connection = connect(user=db_user, host=db_host, password=db_password, database=db_name)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM shows WHERE id IN ' +
                   '(SELECT id_show FROM user_likes WHERE id_user = ' + genre + ') LIMIT 10')
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    shows = list()
    for data in rows:
        show = Show(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9],
                    data[10], data[11], data[12], data[13])
        shows.append(show.serialize())
    return shows

# noinspection SqlResolve
def getUserLikeShows(id_user):
    genre = '\'' + id_user + '\''
    connection = connect(user=db_user, host=db_host, password=db_password, database=db_name)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM shows WHERE id IN ' +
                   '(SELECT id_show FROM user_likes WHERE id_user = ' + genre + ')')
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    shows = list()
    for data in rows:
        show = Show(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9],
                    data[10], data[11], data[12], data[13])
        shows.append(show.serialize())
    return shows

# noinspection SqlResolve
def getShowByID(id):
    connection = connect(user=db_user, host=db_host, password=db_password, database=db_name)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM shows WHERE id = ' + id)
    rows = cursor.fetchall()

    data = rows[0]
    show = Show(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10],
                data[11], data[12],data[13])

    cursor.close()
    connection.close()

    genres = getGenresByShow(data[0])
    if genres is not None:
        show.setGenres(genres)
    creators = getCreatorsByShow(data[0])
    if creators is not None:
        show.setActors(creators)
    actors = getActorsByShow(data[0])
    if actors is not None:
        show.setActors(actors)
    networks = getNetworksByShow(data[0])
    if networks is not None:
        show.setNetworks(networks)

    return show.serialize()

# noinspection SqlResolve
def getShows():
    connection = connect(user=db_user, host=db_host, password=db_password, database=db_name)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM shows')
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

# noinspection SqlResolve
def getHomeShowsByGenre(genre,id):
    genre = '\'' + genre + '\''
    connection = connect(user=db_user, host=db_host, password=db_password, database=db_name)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM shows ' +
                   ' WHERE id IN (SELECT id_show FROM has_genre WHERE id_genre = ' + genre + ')' +
                   ' AND poster IS NOT NULL AND backdrop IS NOT NULL AND language = \'en\' ' +
                   ' AND id NOT IN (SELECT id_show FROM user_likes WHERE id_user = ' + str(id) + ') LIMIT 10')
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    shows = list()
    for data in rows:
        show = Show(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9],
                    data[10], data[11], data[12], data[13])
        shows.append(show.serialize())
    return shows

# noinspection SqlResolve
def getFavoriteGenres(id):
    connection = connect(user=db_user, host=db_host, password=db_password, database=db_name)
    cursor = connection.cursor()
    cursor.execute('SELECT genres.id , genres.genre, count(*) as c FROM user_likes ' +
                   'JOIN shows ON user_likes.id_show = shows.id ' +
                   'JOIN has_genre ON shows.id = has_genre.id_show ' +
                   'JOIN genres ON has_genre.id_genre = genres.id ' +
                   'WHERE user_likes.id_user = ' + str(id) + ' ' +
                   'GROUP BY (genres.id,genres.genre) '
                   'ORDER BY c DESC '
                   'LIMIT 9'
                   )
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    genres = list()
    for data in rows:
        genre = Genre(data[0], data[1])
        genres.append(genre.serialize())
    return genres

# noinspection SqlResolve
def getGenresByShow(id):
    connection = connect(user=db_user, host=db_host, password=db_password, database=db_name)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM genres WHERE id IN (SELECT id_genre FROM has_genre WHERE id_show = ' + str(id) +
                   ' LIMIT 3)')
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    if len(rows) == 0:
        return None

    genres = list()
    for data in rows:
        genre = Genre(data[0], data[1]).serialize()
        genres.append(genre)
    return genres

# noinspection SqlResolve
def getActorsByShow(id):
    connection = connect(user=db_user, host=db_host, password=db_password, database=db_name)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM actors WHERE id IN (SELECT id_actor FROM has_actor WHERE id_show = ' + str(id) +
                   ' LIMIT 3)')
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    if len(rows) == 0:
        return None

    actors = list()
    for data in rows:
        actor = Actor(data[0], data[1]).serialize()
        actors.append(actor)
    return actors

# noinspection SqlResolve
def getNetworksByShow(id):
    connection = connect(user=db_user, host=db_host, password=db_password, database=db_name)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM networks WHERE id IN (SELECT id_network FROM has_network WHERE id_show = ' + str(id) +
                   ' LIMIT 2)')
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    if len(rows) == 0:
        return None

    networks = list()
    for data in rows:
        network = Network(data[0], data[1]).serialize()
        networks.append(network)
    return networks

# noinspection SqlResolve
def getCreatorsByShow(id):
    connection = connect(user=db_user, host=db_host, password=db_password, database=db_name)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM creators WHERE id IN (SELECT id_creator FROM has_creator WHERE id_show = '
                   + str(id) + ')')
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    if len(rows) == 0:
        return None

    creators = list()
    for data in rows:
        creator = Creator(data[0], data[1]).serialize()
        creators.append(creator)
    return creators

# noinspection SqlResolve
def getShowOthersLiked(id_user):
    connection = connect(user=db_user, host=db_host, password=db_password, database=db_name)
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT id_show FROM user_likes WHERE id_show ' +
                   'NOT IN(SELECT id_show FROM user_likes WHERE id_user = ' + str(id_user) + ') ORDER BY id_show')
    rows = [i[0] for i in cursor.fetchall()]
    cursor.close()
    connection.close()

    return rows

# noinspection SqlResolve
def getShowsLiked():
    connection = connect(user=db_user, host=db_host, password=db_password, database=db_name)
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT id_show FROM user_likes ORDER BY id_show')
    rows = [i[0] for i in cursor.fetchall()]
    cursor.close()
    connection.close()

    return rows

# noinspection SqlResolve
def getUsersId():
    connection = connect(user=db_user, host=db_host, password=db_password, database=db_name)
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT id_user FROM user_likes ORDER BY id_user')
    ids = [i[0] for i in cursor.fetchall()]
    cursor.close()
    connection.close()

    return ids

# noinspection SqlResolve
def getUsersShowsId(id_user):
    connection = connect(user=db_user, host=db_host, password=db_password, database=db_name)
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT id_show FROM user_likes WHERE id_user = ' + str(id_user) + ' ORDER BY id_show')
    ids = [i[0] for i in cursor.fetchall()]
    cursor.close()
    connection.close()

    return ids

# noinspection SqlResolve
def signIn(login, password):
    login = '\'' + login + '\''
    password = '\'' + password + '\''
    connection = connect(user=db_user, host=db_host, password=db_password, database=db_name)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE login = ' + login + ' AND password = ' + password)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    if len(rows) == 0:
        return None
    return User(rows[0][0], rows[0][1], rows[0][2]).serialize()

db_user = 'postgres'
db_password = 'postgres'
db_host = 'localhost'
db_name = 'tvshowapp'
