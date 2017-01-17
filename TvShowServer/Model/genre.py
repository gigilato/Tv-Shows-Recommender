class Genre(object):
    def __init__(self, id, genre):
        self.id = id
        self.genre = genre

    def getId(self):
        return self.id

    def getGenre(self):
        return self.genre

    def serialize(self):
        return {'id': self.id, 'genre': self.genre}
