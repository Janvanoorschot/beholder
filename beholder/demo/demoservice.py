from sys import stdout
from twisted.application import service
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor


class DemoService(service.Service):

    def __init__(self, config={}):
        pass

    def startService(self):
        self.endpoint = TCP4ServerEndpoint(reactor, 8007)
        self.endpoint.listen(DemoServerFactory())
        pass

    def stopService(self):
        pass


class DemoServerProtocol(Protocol):

    def dataReceived(self, data):
        stdout.write(data.decode())


class DemoServerFactory (Factory):

    def buildProtocol(self, addr):
        return DemoServerProtocol()

