"""
`astrospice.registry`
---------------------
A registry of SPICE kernels for various missions.
"""
import abc
from collections import defaultdict
from dataclasses import dataclass

import astropy.time
import parfive

from astrospice.config import get_cache_dir
from astrospice.kernel import Kernel

__all__ = ['BaseKernelRegistry', 'RemoteKernel']


class BaseKernelRegistry(abc.ABC):
    """
    Base class for remote registries.

    Kernels are stored in the ``_kernels`` property, which is a dict with
    structure _kernels[body][...][...] -> RemoteKernelsBase. The dict must
    have a first key that specifies the body, and can have more optional keys
    after that (e.g. for SPK kernels this specifies the type of kernel,
    reconstructed or predicted).
    """
    def __init__(self):
        self._kernels = defaultdict(dict)

    def __str__(self):
        return f'Known kernels: {self.bodies}'

    def __getitem__(self, idx):
        return self._kernels[idx]

    @property
    def bodies(self):
        """
        Bodies with available kernels.
        """
        return list(self._kernels.keys())

    def check_body(self, body):
        """
        Raise an error if ``body`` isn't in the registry.
        """
        if body not in self.bodies:
            raise ValueError(
                f'{body} not in list of registered bodies: {self.bodies}')

    @abc.abstractmethod
    def get_available_kernels(self, body):
        """
        Get a list of all available kernels for a given body.

        Returns
        -------
        astropy.table.Table
        """


@dataclass
class RemoteKernel:
    """
    A single kernel available on a remote server.
    """
    url: str
    start_time: astropy.time.Time
    end_time: astropy.time.Time
    version: int

    def __str__(self):
        return '\n'.join([f'URL: {self.url}',
                          f'Start time: {self.start_time.iso}',
                          f'End time: {self.end_time.iso}',
                          f'Version: {self.version}'])

    def __lt__(self, other):
        return self.version < other.version

    @property
    def fname(self):
        """Kernel filename."""
        return self.url.split('/')[-1]

    def fetch(self):
        """
        Get the kernel. If not present locally, will be downloaded.

        This also implicitly furnishes the kernel with SPICE.

        Returns
        -------
        astrospice.KernelBase
        """
        local_path = get_cache_dir() / self.fname
        if not local_path.exists():
            dl = parfive.Downloader()
            dl.enqueue_file(self.url, get_cache_dir(), self.fname)
            dl.download()

        return Kernel(local_path)
