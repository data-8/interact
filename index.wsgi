#!/usr/bin/python3

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/srv/interact/")

from run import app as application
