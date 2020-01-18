from twisted.application import service
from twisted.internet import reactor, defer
import os.path
from twisted.conch.ssh import channel, common

from . import sshclient

class DemoChannel(channel.SSHChannel):

    name = 'session'

    def channelOpen(self, data):
        d = self.conn.sendRequest(self, 'exec', common.NS('ls'), wantReply = 1)
        self.lsData = b''

    def dataReceived(self, data):
        self.lsData += data

    def closed(self):
        print('ls output:', self.lsData)
        self.conn.stop()



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

        def startfinished(connection):
            connection.openChannel(DemoChannel(conn=connection))

        d = defer.ensureDeferred(self.client.start())
        d.addCallback(startfinished)

    def shutdownService(self, somearg):
        reactor.callFromThread(reactor.stop)

    def createEndpoint(self, command):
        pass

    def stopService(self):
        print("service stopped")
