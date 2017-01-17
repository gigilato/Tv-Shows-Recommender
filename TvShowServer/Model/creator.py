class Creator(object):
    def __init__(self, id, creator):
        self.id = id
        self.creator = creator

    def getId(self):
        return self.id

    def getCreator(self):
        return self.creator

    def serialize(self):
        return {'id': self.id, 'creator': self.creator}
