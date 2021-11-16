# Licensed under a 3-clause BSD style license - see LICENSE.rst

from .version import __version__

from .coords import *
from .net import registry
from astrospice.net.generic import setup_generic_files

setup_generic_files()
