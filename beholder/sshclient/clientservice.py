from twisted.application import service
from twisted.internet import reactor, defer
import os.path

from . import sshclient

class ClientService(service.Service):
    """ Simple SSH service heavily based on sshsimpleserver.py from the Twisted docu.
    """

    def __init__(self, config={}):
        self.config = config
        self.client = None

    def startService(self):
        self.client = sshclient.SSHClient(
            self.config['server']['host'],
            int(self.config['server']['port']),
            self.config['server']['fingerprint'].encode(),
            self.config['server']['username'],
            os.path.expanduser(self.config['server']['keypath']),
            os.path.expanduser(self.config['server']['pubkeypath']),
        )
        d = defer.ensureDeferred(self.client.start())
        reactor.callLater(10, self.shutdownService, "some_arg")

    def shutdownService(self, somearg):
        reactor.callFromThread(reactor.stop)

    def createEndpoint(self, command):
        pass

    def stopService(self):
        print("service stopped")
