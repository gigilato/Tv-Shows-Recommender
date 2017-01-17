class User(object):

    def __init__(self, id, login, password):
        self.id = id
        self.login = login
        self.password = password

    def getLogin(self):
        return self.login

    def getId(self):
        return self.id

    def getPassword(self):
        return self.password

    def serialize(self):
        return {'id': self.id, 'login': self.login, 'password': self.password}
