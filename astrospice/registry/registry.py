"""
`astrospice.registry`
---------------------
A registry of SPICE kernels for various missions.
"""
from collections import defaultdict


class KernelRegistry:
    def __init__(self):
        self._kernels = defaultdict(dict)


kernels = KernelRegistry()


class RemoteKernelsBase:
    def __init_subclass__(cls):
        kernels._kernels[cls.name][cls.type] = cls


def get_kernel(name, type=None):
    """
    Get a SPICE kernel.

    If not present locally, will attempt to download.
    """
