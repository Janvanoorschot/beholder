from twisted.conch.endpoints import SSHCommandClientEndpoint
from twisted.internet import reactor

class SSHClient:

    def __init__(self, host, port, username, keys, knownhosts):
        self.host = host
        self.port = port
        self.username = username
        self.keys = keys
        self.knownhosts = knownhosts
        self.reactor = reactor

    def newConnection(self, command):
        return SSHCommandClientEndpoint.newConnection(
            self.reactor, command, self.username, self.host,
            port=self.port, keys=self.keys, knownHosts=self.knownhosts)


