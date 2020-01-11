import os, getpass
from twisted.trial import unittest
from twisted.internet.protocol import Factory, Protocol
from twisted.conch.ssh.keys import EncryptedKeyError, Key
from twisted.internet.task import react
from twisted.conch.client.knownhosts import KnownHostsFile

from beholder.ssh.sshclient import SSHClient

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
        if(data == "come in mork"):
            pass

    def connectionLost(self, reason):
        pass


class SSHTest(unittest.TestCase):

    def __init(self):
        pass

    def testSSH101(self):
        def finished():
            pass
        keys = []
        # keyPath = os.path.abspath('sys/ssh-keys/client_rsa.pub')
        keyPath = '/data/dev/beholder/sys/ssh-keys/client_rsa.pub'
        knownHostsPath = '/home/jan/.ssh/known_hosts'
        if os.path.exists(keyPath):
            keys.append(readKey(keyPath))
        knownHosts = KnownHostsFile.fromPath(knownHostsPath)
        client = SSHClient("localhost", 2222, "user", keys, knownHosts)
        self.assertIsNotNone(client)
        endpoint = client.newConnection("ls")
        self.assertIsNotNone(endpoint)
        factory = Factory()
        factory.protocol = TestProtocol
        d = endpoint.connect(factory)
        d.addCallback(finished)
        return d


