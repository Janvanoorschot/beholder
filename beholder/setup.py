from twisted.logger import Logger
from twisted.application import service
import beholder.demo
from beholder import config

log = Logger()


def createApplication(config_file=config.DEFAULT_CONFIG_FILE):

    log.info("creating beholder application")

    cfg = config.readConfig(config_file)

    application = service.Application(cfg['DEFAULT']['appname'])

    # server application
    serverservice = beholder.demo.TCPDemoServer()
    webservice.setServiceParent(application)

    return application