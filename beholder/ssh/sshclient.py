from twisted.conch.endpoints import SSHCommandClientEndpoint
from twisted.internet import reactor

class SSHClient:

    def __init__(self, host, port, username, keys):
        self.host = host
        self.port = port
        self.username = username
        self.keys = keys

    def newConnection(self, command, protocol):
        return SSHCommandClientEndpoint.newConnection(
            reactor, command, self.username, self.host,
            port=self.port, keys=self.keys)


