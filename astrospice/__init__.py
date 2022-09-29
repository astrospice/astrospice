# Licensed under a 3-clause BSD style license - see LICENSE.rst

import astrospice.time
from astrospice.net.generic import *
from astrospice.net.generic import _setup_generic_files
from .body import *
from .config import *
from .coords import *
from .kernel import *
from .net import registry
from ._version import __version__

_setup_generic_files()
