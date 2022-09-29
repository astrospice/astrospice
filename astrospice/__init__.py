# Licensed under a 3-clause BSD style license - see LICENSE.rst

import astrospice.time
from astrospice.net.generic import *
from astrospice.net.generic import _setup_generic_files
from ._version import __version__
from .body import *
from .config import *
from .coords import *
from .kernel import *
from .net import registry

_setup_generic_files()
