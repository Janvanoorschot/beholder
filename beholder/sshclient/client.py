from twisted.application import service
from twisted.internet import reactor

class ClientService(service.Service):
    """ Simple SSH service heavily based on sshsimpleserver.py from the Twisted docu.
    """

    def __init__(self, config={}):
        self.config = config

    def startService(self):
        reactor.callLater(3.5, self.shutdownService, "some_arg")

    def shutdownService(self, somearg):
        reactor.callFromThread(reactor.stop)

    def createEndpoint(self, command):
        pass

    def stopService(self):
        print("service stopped")
