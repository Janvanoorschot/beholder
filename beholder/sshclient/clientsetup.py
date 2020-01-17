from twisted.logger import Logger
from twisted.application import service
from beholder.sshclient import clientconfig, clientservice

log = Logger()


def createApplication(config_file=clientconfig.DEFAULT_CONFIG_FILE):

    log.info("creating beholder application")

    cfg = clientconfig.readConfig(config_file)

    application = service.Application('sshclient')

    # server application
    serverservice = clientservice.ClientService(cfg)
    serverservice.setServiceParent(application)

    return application