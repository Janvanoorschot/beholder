import configparser
import os.path

DEFAULT_CONFIG_FILE = '/etc/sshclient.conf'

def readConfig(filename):
    defs = {
        "server": {
            "host": "localhost",
            "port": 22,
            "fingerprint": "aa:aa:aa:aa:aa:aa:aa:aa:aa:aa:aa:aa:aa:aa:aa:aa"
        },
    }
    cfg = configparser.ConfigParser()
    cfg.read_dict(defs)
    if os.path.exists(filename):
        cfg.read(filename)
    return cfg