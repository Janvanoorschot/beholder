#!/usr/bin/env python

import sys
import os
import logging
logging.basicConfig(level=logging.INFO)
sys.path.insert(0, os.path.abspath(os.getcwd()))

from beholder.sshclient import clientsetup

configfile = os.environ.get('TAC_CONFIGFILE')
application = clientsetup.createApplication(configfile)
