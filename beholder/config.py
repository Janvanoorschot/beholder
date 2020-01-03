import configparser

DEFAULT_CONFIG_FILE = '/etc/beholder.conf'
APP_NAME = 'beholder'

def readConfig(filename):
    defs = {
        "host": {
            "host1": "value1_host1"
        },
        "output": {
            "output1": "value_output1"
        }
    }
    cfg = configparser.ConfigParser()
    cfg.read_dict(defs)
    cfg.read(filename)
    return cfg