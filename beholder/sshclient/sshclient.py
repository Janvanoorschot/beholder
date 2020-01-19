from twisted.internet import defer, protocol, reactor, endpoints
from twisted.conch.ssh import connection, userauth, keys, transport
from twisted.conch.ssh.transport import DISCONNECT_BY_APPLICATION
from twisted.conch import error as concherror


class SSHClient:
    """ Conch client interface.

    See https://twistedmatrix.com/documents/current/conch/howto/conch_client.html starting at section
    'Writing the client' (so not the more limited SSHCommandClientEndpoint). To quote that documentation:
        Writing a client with Conch involves sub-classing 4 classes:
            * twisted.conch.ssh.transport.SSHClientTransport (plus  protocol.ClientFactory)
            * twisted.conch.ssh.connection.SSHConnection
            * twisted.conch.ssh.userauth.SSHUserAuthClient
            * twisted.conch.ssh.channel.SSHChannel
    Note that the use the SSHChannel is kept outside this module and should be implemented by the caller.
    The async 'start' call returns the 'SSHConnection' connection which can be used to attach an SSHChannel
    using the 'openChannel' call.
    """

    def __init__(self, host, port, fingerprint, username, keypath, pubkeypath):
        self.host = host
        self.port = port
        self.fingerprint = fingerprint
        self.username = username
        self.keypath = keypath
        self.pubkeypath = pubkeypath
        #
        self.transport = None
        self.connection = None

    async def start(self):
        self.transport = await self._createTCPConnection()
        # we now have an SSH client_transport/connection with fingerprint checked (connection_secure_d). No auth yet.
        # Over this transport
        self.connection = SSHConnection()
        self.transport.requestService(
            UserAuthClient(
                self.username,
                self.connection,
                self.pubkeypath,
                self.keypath
            ))
        await self.connection.ready()
        return self.connection

    async def stop(self):
        self.transport.sendDisconnect(DISCONNECT_BY_APPLICATION, "done")

    def _createTCPConnection(self):

        def hostVerified(proto):
            return proto

        def gotProtocol(proto):
            proto.connection_secure_d.addCallback(hostVerified)
            return proto.connection_secure_d

        factory = SSHClientFactory(self.fingerprint)
        endpoint = endpoints.TCP4ClientEndpoint(reactor, self.host, self.port)
        d = endpoint.connect(factory)
        d.addCallback(gotProtocol)
        return d


class SSHClientTransport(transport.SSHClientTransport):
    # SSHClientTransport implements the client side of the SSH protocol

    def __init__(self, fingerprint):
        self.fingerprint = fingerprint
        self.connection_secure_d = defer.Deferred()

    def verifyHostKey(self, public_key, fingerprint):
        if fingerprint == self.fingerprint:
            return defer.succeed(1)
        else:
            return defer.fail(concherror.ConchError('host key failure'))

    def connectionSecure(self):
        self.connection_secure_d.callback(self)


class SSHClientFactory(protocol.ClientFactory):

    def __init__(self, fingerprint):
        self.protocol = SSHClientTransport
        self.fingerprint = fingerprint
        self.stopped = False

    def buildProtocol(self, addr):
        p = self.protocol(self.fingerprint)
        p.factory = self
        return p

    def stopFactory(self):
        self.stopped = True


class SSHConnection(connection.SSHConnection):

    def __init__(self):
        connection.SSHConnection.__init__(self)
        self.ssh_connection_established_d = defer.Deferred()

    def serviceStarted(self):
        self.ssh_connection_established_d.callback(self)

    def ready(self):
        return self.ssh_connection_established_d


class UserAuthClient(userauth.SSHUserAuthClient):

    def __init__(self, user, connection, public_key_path, private_key_path):
        userauth.SSHUserAuthClient.__init__(self, user, connection)
        self.public_key_path  = public_key_path
        self.private_key_path = private_key_path

    def getPassword(self, prompt=None):
        return  # no password authentication

    def getPublicKey(self):
        return keys.Key.fromFile(self.public_key_path)

    def getPrivateKey(self):
        return defer.succeed( keys.Key.fromFile(self.private_key_path) )


