class Network(object):

    def __init__(self,id, network):
        self.id = id
        self.network = network

    def getId(self):
        return self.id

    def getNetwork(self):
        return self.network

    def serialize(self):
        return {'id': self.id, 'network': self.network}
