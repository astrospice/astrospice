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

    def __getitem__(self, idx):
        return self._kernels[idx]

    @property
    def names(self):
        return list(self._kernels.keys())

    def get_remote_kernels(self, name, type):
        return self._kernels[name][type].get_remote_kernels()


registry = KernelRegistry()


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

    def __lt__(self, other):
        return self.version < other.version


class RemoteKernelsBase:
    def __init_subclass__(cls):
        registry._kernels[cls.name][cls.type] = cls()

    def get_latest_kernel(self):
        """
        Download the latest version of the kernel.
        """
        kernels = self.get_remote_kernels()
        latest_kernel = sorted(kernels)[-1]
