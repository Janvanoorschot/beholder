#!/usr/bin/env python

import sys
import os
import socket
import logging
logging.basicConfig(level=logging.INFO)

# prague == 'opennsa-agents'
# raspie == 'raspie'
if socket.gethostname() == 'raspie':
    import ptvsd
    ptvsd.enable_attach(address=('192.168.1.16', 3343), redirect_output=True)
    ptvsd.wait_for_attach()

sys.path.insert(0, os.path.abspath(os.getcwd()))

from beholder import setup

application = setup.createApplication('bin/beholder.conf')
