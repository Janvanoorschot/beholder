from sys import stdout
from zope.interface import implementer

from twisted.application import service
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

from twisted.internet import reactor, protocol
from twisted.python import components

from twisted.cred import portal as ptl
from twisted.cred.checkers import InMemoryUsernamePasswordDatabaseDontUse

from twisted.conch import avatar
from twisted.conch.ssh import factory, connection, keys, userauth, session
from twisted.conch.checkers import SSHPublicKeyChecker, InMemorySSHKeyDB

class SSHService(service.Service):
    """ Simple SSH service heavily based on sshsimpleserver.py from the Twisted docu.
    """

    def __init__(self, config={}):
        self.config = config

    def startService(self):
        components.registerAdapter(SSHSession, SSHAvatar, session.ISession)
        portal = ptl.Portal(SSHRealm())
        passwdDB = InMemoryUsernamePasswordDatabaseDontUse()
        passwdDB.addUser(b'user', b'password')
        sshDB = SSHPublicKeyChecker(InMemorySSHKeyDB(
            {b'user': [keys.Key.fromFile(CLIENT_RSA_PUBLIC)]}))
        portal.registerChecker(passwdDB)
        portal.registerChecker(sshDB)
        SSHServerFactory.portal = portal
        self.endpoint = TCP4ServerEndpoint(reactor, 2222)
        self.endpoint.listen(SSHServerFactory())

    def createEndpoint(self, command):
        pass
    
    def stopService(self):
        pass


PRIMES = {
    2048: [(2, 24265446577633846575813468889658944748236936003103970778683933705240497295505367703330163384138799145013634794444597785054574812547990300691956176233759905976222978197624337271745471021764463536913188381724789737057413943758936963945487690939921001501857793275011598975080236860899147312097967655185795176036941141834185923290769258512343298744828216530595090471970401506268976911907264143910697166165795972459622410274890288999065530463691697692913935201628660686422182978481412651196163930383232742547281180277809475129220288755541335335798837173315854931040199943445285443708240639743407396610839820418936574217939)],
    4096: [(2, 889633836007296066695655481732069270550615298858522362356462966213994239650370532015908457586090329628589149803446849742862797136176274424808060302038380613106889959709419621954145635974564549892775660764058259799708313210328185716628794220535928019146593583870799700485371067763221569331286080322409646297706526831155237865417316423347898948704639476720848300063714856669054591377356454148165856508207919637875509861384449885655015865507939009502778968273879766962650318328175030623861285062331536562421699321671967257712201155508206384317725827233614202768771922547552398179887571989441353862786163421248709273143039795776049771538894478454203924099450796009937772259125621285287516787494652132525370682385152735699722849980820612370907638783461523042813880757771177423192559299945620284730833939896871200164312605489165789501830061187517738930123242873304901483476323853308396428713114053429620808491032573674192385488925866607192870249619437027459456991431298313382204980988971292641217854130156830941801474940667736066881036980286520892090232096545650051755799297658390763820738295370567143697617670291263734710392873823956589171067167839738896249891955689437111486748587887718882564384870583135509339695096218451174112035938859)],
    }
SERVER_RSA_PRIVATE = 'sys/ssh-keys/ssh_host_rsa_key'
SERVER_RSA_PUBLIC = 'sys/ssh-keys/ssh_host_rsa_key.pub'
CLIENT_RSA_PUBLIC = 'sys/ssh-keys/client_rsa.pub'

@implementer(ptl.IRealm)
class SSHRealm(object):
    def requestAvatar(self, avatarId, mind, *interfaces):
        return interfaces[0], SSHAvatar(avatarId), lambda: None

class SSHServerFactory(factory.SSHFactory):
    publicKeys = {
        b'ssh-rsa': keys.Key.fromFile(SERVER_RSA_PUBLIC)
    }
    privateKeys = {
        b'ssh-rsa': keys.Key.fromFile(SERVER_RSA_PRIVATE)
    }
    # Service handlers.
    services = {
        b'ssh-userauth': userauth.SSHUserAuthServer,
        b'ssh-connection': connection.SSHConnection
    }

    def getPrimes(self):
        """
        See: L{factory.SSHFactory}
        """
        return PRIMES

class SSHAvatar(avatar.ConchUser):
    def __init__(self, username):
        avatar.ConchUser.__init__(self)
        self.username = username
        self.channelLookup.update({b'session':session.SSHSession})

class SSHSession(object):

    def __init__(self, avatar):
        pass

    def getPty(self, term, windowSize, attrs):
        pass


    def execCommand(self, proto, cmd):
        raise Exception("not executing commands")

    def openShell(self, transport):
        protocol = EchoProtocol()
        protocol.makeConnection(transport)
        transport.makeConnection(session.wrapProtocol(protocol))

    def eofReceived(self):
        pass

    def closed(self):
        pass

class EchoProtocol(protocol.Protocol):

    def dataReceived(self, data):
d        if data == b'\r':
            data = b'\r\n'
        elif data == b'\x03': #^C
            self.transport.loseConnection()
            return
        self.transport.write(data)


