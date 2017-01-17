class Actor(object):

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def getName(self):
        return self.name

    def getId(self):
        return self.id

    def serialize(self):
        return {'id': self.id, 'name': self.name}
