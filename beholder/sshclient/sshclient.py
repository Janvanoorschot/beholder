from twisted.internet import defer, protocol, reactor, endpoints
from twisted.conch.ssh import connection, userauth, keys, transport
from twisted.conch import error as concherror
from twisted.conch.ssh import channel, common


class SSHClient:

    def __init__(self, host, port, fingerprint, username, keypath, pubkeypath):
        self.host = host
        self.port = port
        self.fingerprint = fingerprint
        self.username = username
        self.keypath = keypath
        self.pubkeypath = pubkeypath
        self.connection = None

    async def start(self):
        tcp = await self._createTCPConnection()
        self.connection = SSHConnection()
        tcp.requestService(
            UserAuthClient(
                self.username,
                self.connection,
                self.pubkeypath,
                self.keypath
            ))
        # return self.connection.ssh_connection_established_d
        # return tcp.connection_secure_d

    async def stop(self):
        pass

    def _createTCPConnection(self):

        def hostVerified(client, proto):
            return proto

        def gotProtocol(proto):
            proto.connection_secure_d.addCallback(hostVerified, proto)
            self.proto = proto
            return proto.connection_secure_d

        factory = SSHClientFactory(self.fingerprint)
        endpoint = endpoints.TCP4ClientEndpoint(reactor, self.host, self.port)
        d = endpoint.connect(factory)
        d.addCallback(gotProtocol)
        return d


class SSHConnection(connection.SSHConnection):

    def __init__(self):
        connection.SSHConnection.__init__(self)
        self.ssh_connection_established_d = defer.Deferred()

    def serviceStarted(self):
        self.openChannel(DemoChannel(conn = self))
        self.ssh_connection_established_d.callback(self)

class DemoChannel(channel.SSHChannel):

    name = 'session'

    def channelOpen(self, data):
        d = self.conn.sendRequest(self, 'exec', common.NS('ls'), wantReply = 1)
        self.lsData = b''

    def dataReceived(self, data):
        self.lsData += data

    def closed(self):
        print('ls output:', self.lsData)


class UserAuthClient(userauth.SSHUserAuthClient):

    def __init__(self, user, connection, public_key_path, private_key_path):
        userauth.SSHUserAuthClient.__init__(self, user, connection)
        self.public_key_path  = public_key_path
        self.private_key_path = private_key_path

    def getPassword(self, prompt=None):
        return # no password authentication

    def getPublicKey(self):
        return keys.Key.fromFile(self.public_key_path)

    def getPrivateKey(self):
        return defer.succeed( keys.Key.fromFile(self.private_key_path) )


class SSHClientTransport(transport.SSHClientTransport):

    def __init__(self, fingerprint):
        self.fingerprint = fingerprint
        self.connection_secure_d = defer.Deferred()

    def verifyHostKey(self, public_key, fingerprint):
        if fingerprint == self.fingerprint:
            return defer.succeed(1)
        else:
            return defer.fail(concherror.ConchError('host key failure'))

    def connectionSecure(self):
        print("connectionSecure")
        self.connection_secure_d.callback(self)


class SSHClientFactory(protocol.ClientFactory):

    protocol = SSHClientTransport

    def __init__(self, fingerprint):
        self.fingerprint = fingerprint
        self.stopped = False

    def buildProtocol(self, addr):
        p = self.protocol(self.fingerprint)
        p.factory = self
        return p

    def stopFactory(self):
        self.stopped = True


