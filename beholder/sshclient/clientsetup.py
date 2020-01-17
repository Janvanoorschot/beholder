from twisted.logger import Logger
from twisted.application import service
from beholder.sshclient import clientconfig, client

log = Logger()


def createApplication(config_file=clientconfig.DEFAULT_CONFIG_FILE):

    log.info("creating beholder application")

    cfg = clientconfig.readConfig(config_file)

    application = service.Application(cfg['DEFAULT']['appname'])

    # server application
    serverservice = client.ClientService()
    serverservice.setServiceParent(application)

    return application