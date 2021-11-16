# Licensed under a 3-clause BSD style license - see LICENSE.rst

from astrospice.net.generic import setup_generic_files
from .coords import *
from .net import registry
import astrospice.time
from .version import __version__

setup_generic_files()
