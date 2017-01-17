from urllib2 import urlopen, HTTPError
import json
from psycopg2 import *
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def escapeChar(string):
    res = ""
    for char in string:
        if char == '\'':
            res += '\''
        res += char
    return res

def getName(data):
    return '\'' + escapeChar(data['name']) + '\''

def getNetworks(data):
    networks = list()
    for network in data['networks']:
        networks.append('\'' + escapeChar(network['name']) + '\'')
    return networks

def getPoster(data):
    if data['poster_path'] is None:
        return 'NULL'
    return '\'image.tmdb.org/t/p/w500' + str(data['poster_path']) + '\''

def getBackdrop(data):
    if data['backdrop_path'] is None:
        return 'NULL'
    return '\'image.tmdb.org/t/p/w500' + str(data['backdrop_path']) + '\''

def getOverview(data):
    if data['overview'] == '' or data['overview'] is None:
        return 'NULL'
    return '\'' + escapeChar(data['overview']) + '\''

def getType(data):
    if data['type'] == '' or data['type'] is None:
        return 'NULL'
    return '\'' + escapeChar(data['type']) + '\''

def getGenre(data):
    genres = list()
    for genre in data['genres']:
        genres.append('\'' + escapeChar(genre['name']) + '\'')
    return genres

def getCreatedBy(data):
    creators = list()
    for creator in data['created_by']:
        creators.append('\'' + escapeChar(creator['name']) + '\'')
    return creators

def getLanguage(data):
    if len(data['languages']) != 0:
        return '\'' + data['languages'][0] + '\''
    return 'NULL'

def getSeasonNb(data):
    if data['number_of_seasons'] == '' or data['number_of_seasons'] is None:
        return 'NULL'
    return str(data['number_of_seasons'])

def getDate(data):
    if data['first_air_date'] is None:
        return 'NULL'
    return '\'' + data['first_air_date'] + '\''

def getEpisodeNb(data):
    if data['number_of_episodes'] == '' or data['number_of_episodes'] is None:
        return 'NULL'
    return str(data['number_of_episodes'])

def getRunTime(data):
    if len(data['episode_run_time']) != 0:
        return str(data['episode_run_time'][0])
    return '0'

def getStatus(data):
    if data['status'] == '' or data['status'] is None:
        return 'NULL'
    return '\'' + escapeChar(data['status']) + '\''

def getPopularity(data):
    if data['popularity'] == '0.0':
        return 'NULL'
    return str(data['popularity'])

def getVotes(data):
    if data['vote_average'] == '0.0':
        return 'NULL'
    return str(data['vote_average'])

def getCast(data):
    actors = list()
    for actor in data['credits']['cast']:
        actors.append('\'' + escapeChar(actor['name']) + '\'')
    return actors

# noinspection SqlResolve
def createDatabase():
    connection = connect(user=db_user, host=db_host, password=db_password)

    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()

    cursor.execute('DROP DATABASE tvshowapp')
    cursor.execute('CREATE DATABASE tvshowapp')

    cursor.close()
    connection.close()


# noinspection SqlResolve
def createTables():
    connection = connect(user=db_user, host=db_host, password=db_password, database=db_name)
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE shows('
                   'id SERIAL PRIMARY KEY,'
                   'name TEXT NULL,'
                   'poster TEXT NULL,'
                   'overview TEXT NULL,'
                   'type TEXT NULL DEFAULT \'unknown\','
                   'language VARCHAR(2) NULL,'
                   'seasons INT NULL DEFAULT 0,'
                   'episodes INT NULL DEFAULT 0,'
                   'runtime INT NULL DEFAULT 0,'
                   'status TEXT NULL DEFAULT \'unknown\','
                   'air_date DATE NULL,'
                   'popularity NUMERIC NULL DEFAULT 0.0,'
                   'votes NUMERIC NULL DEFAULT 0.0,'
                   'backdrop TEXT NULL)'
                   )

    cursor.execute('CREATE TABLE genres('
                   'id SERIAL PRIMARY KEY ,'
                   'genre TEXT NOT NULL)'
                   )

    cursor.execute('CREATE TABLE networks('
                   'id SERIAL PRIMARY KEY ,'
                   'network TEXT NOT NULL)'
                   )

    cursor.execute('CREATE TABLE creators('
                   'id SERIAL PRIMARY KEY ,'
                   'creator TEXT NOT NULL)'
                   )

    cursor.execute('CREATE TABLE users('
                   'id SERIAL PRIMARY KEY ,'
                   'login TEXT NOT NULL UNIQUE,'
                   'password TEXT NOT NULL)'
                   )

    cursor.execute('CREATE TABLE actors('
                   'id SERIAL PRIMARY KEY ,'
                   'actor TEXT NOT NULL UNIQUE)'
                   )

    cursor.execute('CREATE TABLE has_genre('
                   'id_show INT REFERENCES shows(id) ON DELETE CASCADE ,'
                   'id_genre INT REFERENCES genres(id) ON DELETE CASCADE ,'
                   'PRIMARY KEY (id_show,id_genre))'
                   )

    cursor.execute('CREATE TABLE has_network('
                   'id_show INT REFERENCES shows(id) ON DELETE CASCADE ,'
                   'id_network INT REFERENCES networks(id) ON DELETE CASCADE ,'
                   'PRIMARY KEY (id_show,id_network))'
                   )

    cursor.execute('CREATE TABLE has_creator('
                   'id_show INT REFERENCES shows(id) ON DELETE CASCADE ,'
                   'id_creator INT REFERENCES creators(id) ON DELETE CASCADE ,'
                   'PRIMARY KEY (id_show,id_creator))'
                   )

    cursor.execute('CREATE TABLE user_likes('
                   'id_show INT REFERENCES shows(id) ON DELETE CASCADE ,'
                   'id_user INT REFERENCES users(id) ON DELETE CASCADE ,'
                   'PRIMARY KEY (id_show,id_user))'
                   )

    cursor.execute('CREATE TABLE has_actor('
                   'id_show INT REFERENCES shows(id) ON DELETE CASCADE ,'
                   'id_actor INT REFERENCES actors(id) ON DELETE CASCADE ,'
                   'PRIMARY KEY (id_show,id_actor))'
                   )

    connection.commit()
    cursor.close()
    connection.close()

# noinspection SqlResolve
def addShowToDatabase(cursor,show,i):
    cursor.execute(
        'INSERT INTO shows(id,name,poster,overview,type,language,seasons,episodes,runtime,status'
        ',air_date,popularity,votes,backdrop)' +
        'VALUES(' + str(i) + ',' + getName(show) + ',' + getPoster(show) + ',' + getOverview(show) + ',' +
        getType(show) + ',' + getLanguage(show) + ',' + getSeasonNb(show) + ',' +
        getEpisodeNb(show) + ',' + getRunTime(show) + ',' + getStatus(show) + ',' + getDate(show) + ',' +
        getPopularity(show) + ',' + getVotes(show) + ',' + getBackdrop(show) + ')'
    )

    for genre in getGenre(show):
        cursor.execute('SELECT id FROM genres WHERE genre = ' + genre)
        rows = cursor.fetchall()
        if len(rows) == 0:
            cursor.execute('INSERT INTO genres(genre) VALUES (' + genre + ')')
        cursor.execute('SELECT id FROM genres WHERE genre = ' + genre)
        rows = cursor.fetchall()
        genre_id = rows[0][0]
        cursor.execute('INSERT INTO has_genre VALUES (' + str(i) + ',' + str(genre_id) +
                       ') ON CONFLICT DO NOTHING')

    for network in getNetworks(show):
        cursor.execute('SELECT id FROM networks WHERE network = ' + network)
        rows = cursor.fetchall()
        if len(rows) == 0:
            cursor.execute('INSERT INTO networks(network) VALUES (' + network + ')')
        cursor.execute('SELECT id FROM networks WHERE network = ' + network)
        rows = cursor.fetchall()
        network_id = rows[0][0]
        cursor.execute('INSERT INTO has_network VALUES (' + str(i) + ',' + str(network_id) +
                       ') ON CONFLICT DO NOTHING')

    for creator in getCreatedBy(show):
        cursor.execute('SELECT id FROM creators WHERE creator = ' + creator)
        rows = cursor.fetchall()
        if len(rows) == 0:
            cursor.execute('INSERT INTO creators(creator) VALUES (' + creator + ')')
        cursor.execute('SELECT id FROM creators WHERE creator = ' + creator)
        rows = cursor.fetchall()
        creator_id = rows[0][0]
        cursor.execute('INSERT INTO has_creator VALUES (' + str(i) + ',' + str(creator_id) +
                       ') ON CONFLICT DO NOTHING')

    for actor in getCast(show):
        cursor.execute('SELECT id FROM actors WHERE actor = ' + actor)
        rows = cursor.fetchall()
        if len(rows) == 0:
            cursor.execute('INSERT INTO actors(actor) VALUES (' + actor + ')')
        cursor.execute('SELECT id FROM actors WHERE actor = ' + actor)
        rows = cursor.fetchall()
        actor_id = rows[0][0]
        cursor.execute('INSERT INTO has_actor VALUES (' + str(i) + ',' + str(actor_id) +
                       ') ON CONFLICT DO NOTHING')

def fillDatabase():
    connection = connect(user=db_user, host=db_host, password=db_password, database=db_name)
    cursor = connection.cursor()

    i = 9197
    for id_show in range(52165, 63000):
        try:
            url = 'https://api.themoviedb.org/3/tv/'+str(id_show) +\
                  '?api_key=c796280688396e36c2a39b727d309853&append_to_response=credits'
            show = json.loads(urlopen(url).read().decode('ascii', 'ignore'))

            if show['overview'] is None or show['overview'] == "" or show['name'] == "" or show['name'] is None \
                    or show['poster_path'] is None or show['backdrop_path'] is None or show['languages'] is None\
                    or show['languages'] == "":
                continue

            addShowToDatabase(cursor,show,i)
            print str(i) + " : " + str(id_show)
            connection.commit()
            i += 1
        except UnicodeDecodeError:
            pass
        except HTTPError:
            pass

    cursor.close()
    connection.close()

if __name__ == '__main__':
    db_user = 'postgres'
    db_password = 'postgres'
    db_host = 'localhost'
    db_name = 'tvshowapp'

    """createDatabase()
    createTables()
    fillDatabase()"""
