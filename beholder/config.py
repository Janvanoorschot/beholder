import configparser

DEFAULT_CONFIG_FILE = '/etc/beholder.conf'

def readConfig(filename):
    defs = {
        "DEFAULT": {
            "appname": "beholder"
        },
        "server": {
            "host": "localhost",
            "port": 22
        },
        "output": {
            "file": "file.out"
        }
    }
    cfg = configparser.ConfigParser()
    cfg.read_dict(defs)
    cfg.read(filename)
    return cfg