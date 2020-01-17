from twisted.conch.endpoints import SSHCommandClientEndpoint
from twisted.internet import reactor

class SSHCmdClient:

    def __init__(self, host, port, username, keys=None, knownhosts=None, agent=None, reactor=reactor):
        self.host = host
        self.port = port
        self.username = username
        self.keys = keys
        self.knownhosts = knownhosts
        self.agent=agent
        self.reactor = reactor

    def newConnection(self, command):
        return SSHCommandClientEndpoint.newConnection(
            self.reactor, command, self.username, self.host,
            port=self.port, keys=self.keys, knownHosts=self.knownhosts)


