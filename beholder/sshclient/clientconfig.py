import configparser
import os.path

DEFAULT_CONFIG_FILE = '/etc/sshclient.conf'

def readConfig(filename):
    defs = {
        "DEFAULT": {
            "appname": "sshclient"
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
    if os.path.exists(filename):
        cfg.read(filename)
    return cfg