"""
`astrospice.registry`
---------------------
A registry of SPICE kernels for various missions.
"""
from collections import defaultdict
from dataclasses import dataclass

from astropy.time import Time


class KernelRegistry:
    def __init__(self):
        self._kernels = defaultdict(dict)


kernels = KernelRegistry()


@dataclass
class RemoteKernel:
    url: str
    start_time: Time
    end_time: Time
    version: int

    def __str__(self):
        return '\n'.join([f'URL: {self.url}',
                f'Start time: {self.start_time.iso}',
                f'End time: {self.end_time.iso}',
                f'Version: {self.version}'])


class RemoteKernelsBase:
    def __init_subclass__(cls):
        kernels._kernels[cls.name][cls.type] = cls


def get_kernel(name, type=None):
    """
    Get a SPICE kernel.

    If not present locally, will attempt to download.
    """
