class Show(object):
    def __init__(self,id,name,poster,overview,type,language,seasons,episodes,runtime,status,airDate,popularity,votes,backdrop):
        self.id = id
        self.name = name
        self.poster = poster
        self.overview = overview
        self.type = type
        self.language = language
        self.seasons = seasons
        self.episodes = episodes
        self.runtime = runtime
        self.status = status
        self.airDate = airDate
        self.popularity = popularity
        self.votes = votes
        self.backdrop = backdrop
        self.networks = ''
        self.creators = ''
        self.genres = ''
        self.actors = ''

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getPoster(self):
        return self.poster

    def getOverview(self):
        return self.overview

    def getType(self):
        return self.type

    def getLanguage(self):
        return self.language

    def getSeasons(self):
        return self.seasons

    def getEpisodes(self):
        return self.episodes

    def getRuntime(self):
        return self.runtime

    def getStatus(self):
        return self.status

    def getAirDate(self):
        return self.airDate

    def getPopularity(self):
        return self.popularity

    def getVotes(self):
        return self.votes

    def getBackdrop(self):
        return self.backdrop

    def getActors(self):
        return self.actors

    def getCreators(self):
        return self.creators

    def getGenres(self):
        return self.genres

    def getNetworks(self):
        return self.networks

    def setActors(self,actors):
        self.actors = actors

    def setCreators(self, creators):
        self.creators = creators

    def setGenres(self, genres):
        self.genres = genres

    def setNetworks(self, networks):
        self.networks = networks

    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'poster': self.poster,
                'overview': self.overview,
                'type': self.type,
                'language': self.language,
                'seasons': self.seasons,
                'episodes': self.episodes,
                'runtime': self.runtime,
                'status': self.status,
                'airDate': self.airDate,
                'popularity': self.popularity,
                'votes': self.votes,
                'backdrop': self.backdrop,
                'networks': self.networks,
                'creators': self.creators,
                'genres': self.genres,
                'actors': self.actors
                }
