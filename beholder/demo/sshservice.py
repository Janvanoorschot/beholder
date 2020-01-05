from sys import stdout
from twisted.application import service
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from twisted.conch.endpoints import EndSSHCommandClientEndpoint



class SSHService(service.Service):

    def __init__(self, config={}):
        self.config = config

    def startService(self):
        self.endpoint = TCP4ServerEndpoint(reactor, 8007)
        self.endpoint.listen(DemoServerFactory())

    def createEndpoint(self, command):
        return SSHCommandClientEndpoint.newConnection(
            self.reactor, 
            command, 
            self.username, 
            self.host,
            port=self.port, 
            keys=self.keys, 
            password=self.password,
            agentEndpoint=self.agent, 
            knownHosts=self.knownHosts
            )
    
    def stopService(self):
        pass


class DemoServerProtocol(Protocol):

    def dataReceived(self, data):
        stdout.write(data.decode())


class DemoServerFactory (Factory):

    def buildProtocol(self, addr):
        return DemoServerProtocol()

