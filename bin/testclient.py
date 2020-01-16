from beholder import ensure_deferred
from beholder.ssh import SSHClient
import os.path
from twisted.python import log
from twisted.internet import defer, reactor
import asyncio

host = 'raspie.lan'
port = 22
fingerprint = b'4a:32:2d:09:8a:7e:03:4c:d9:ab:95:a3:c0:cd:2a:56'
username = 'jan'
keypath= '~/.ssh/sshclient_rsa'
pubkeypath= '~/.ssh/sshclient_rsa.pub'


async def doMain():
    client = SSHClient(host, port, fingerprint, username, os.path.expanduser(keypath), os.path.expanduser(pubkeypath))
    await client.start()

def main():

    def slightlyDelayedShutdown(_):
        print("shutdown")
        # reactor.callLater(0.1, reactor.stop)

    def printError(error):
        print("error")
        log.err(error)

    d = defer.ensureDeferred(doMain())
    d.addErrback(printError)
    d.addBoth(slightlyDelayedShutdown)
    return d



if __name__ == '__main__':
    reactor.callWhenRunning(main)
    reactor.run()
