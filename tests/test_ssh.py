import os, getpass
from twisted.trial import unittest
from twisted.internet import reactor
from twisted.python.filepath import FilePath

from twisted.internet.protocol import Factory, Protocol
from twisted.conch.ssh.keys import EncryptedKeyError, Key
from twisted.internet.task import react
from twisted.conch.client.knownhosts import KnownHostsFile
from twisted.internet.endpoints import UNIXClientEndpoint


from beholder.ssh.sshcmdclient import SSHCmdClient

def readKey(path):
    try:
        return Key.fromFile(path)
    except EncryptedKeyError:
        passphrase = getpass.getpass("%r keyphrase: " % (path,))
        return Key.fromFile(path, passphrase=passphrase)

class TestProtocol(Protocol):
    
    def connectionMade(self):
        self.transport.write("mork calling orson")

    def dataReceived(self, data):
        self.transport.loseConnection()

    def connectionLost(self, reason):
        pass


class SSHTest(unittest.TestCase):

    def __init(self):
        pass

    def testSSH101(self):
        def finished():
            pass
        keypaths = [
            # '/data/dev/beholder/sys/ssh-keys/client_rsa.pub',
            '/data/dev/beholder/sys/ssh-keys/client_rsa'
        ]
        keys = []
        for keyPath in keypaths:
            if os.path.exists(keyPath):
                keys.append(readKey(keyPath))
        knownHostsPath = '/home/jan/.ssh/known_hosts'
        knownHosts = KnownHostsFile.fromPath(FilePath(knownHostsPath))
        # for entry in knownHosts.iterentries():
        #     if entry.matchesHost(b"[localhost]:2222"):
        #         print("yess!!!!!!!!!!!!!!!!!!!!!")
        #         print(entry)
        agentEndpoint = UNIXClientEndpoint(reactor, os.environ["SSH_AUTH_SOCK"])
        client = SSHCmdClient(
            b"localhost", 2222, b"user", 
            keys=keys, knownhosts=knownHosts, agent=None)
        self.assertIsNotNone(client)
        endpoint = client.newConnection("ls")
        self.assertIsNotNone(endpoint)
        factory = Factory()
        factory.protocol = TestProtocol
        d = endpoint.connect(factory)
        d.addCallback(finished)
        return d


