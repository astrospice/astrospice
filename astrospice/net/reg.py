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
from astropy.table import Table, vstack
from astropy.time import Time

from astrospice.config import get_cache_dir
from astrospice.kernel import SPKKernel

__all__ = ['KernelRegistry', 'RemoteKernel', 'RemoteKernelsBase', 'registry']


class KernelRegistry:
    """
    A registry of remote SPICE kernels.

    Kernels are stored in the ``_kernels`` property, which is a dict with
    structure _kernels[body][type] -> RemoteKernelsBase
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

    def get_available_kernels(self, body):
        """
        Get all the available kernels.

        Parameters
        ----------
        body : str
        type : str

        Returns
        -------
        astropy.table.Table
        """
        tables = []
        for type in self._kernels[body]:
            kernels = self._kernels[body][type].get_remote_kernels()
            urls = [k.url for k in kernels]
            stimes = Time([k.start_time for k in kernels])
            etimes = Time([k.end_time for k in kernels])
            versions = [k.version for k in kernels]
            tables.append(Table({'Mission': [body] * len(urls),
                                 'Type': [type] * len(urls),
                                 'Version': versions,
                                 'Start time': stimes,
                                 'End time': etimes}))

        tables = vstack(tables)
        tables['Start time'].format = 'iso'
        tables['End time'].format = 'iso'
        return tables

    def get_latest_kernel(self, body, type):
        """
        Returns
        -------
        astrospice.SPKKernel
        """
        self.check_body(body)
        return self._kernels[body][type].get_latest_kernel()

    def get_kernels(self, body, type, *, version=None):
        """
        Get a set of kernels. Any kernels not present locally will be
        downloaded.

        Parameters
        ----------
        body : str
            Spacecraft body.
        type : str
            ``'recon'`` or ``'pred'`` to downloaded reconstructed or predicted
            kernels respectively.
        version : int, optional
            If given, get only kernels with this version.

        Returns
        -------
        list[pathlib.Path]
            List of local filepaths.
        """
        self.check_body(body)
        types = list(self._kernels[body].keys())
        if type not in types:
            raise ValueError(f'{type} is not one of the known kernel types '
                             f'for {body}: {types}')
        return self._kernels[body][type].get_kernels(version=version)


registry = KernelRegistry()


@dataclass
class RemoteKernel:
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
        return self.url.split('/')[-1]

    def fetch(self):
        """
        Get the kernel. If not present locally, will be downloaded.

        Returns
        -------
        astrospice.SPKKernel
        """
        local_path = get_cache_dir() / self.fname
        if not local_path.exists():
            dl = parfive.Downloader()
            dl.enqueue_file(self.url, get_cache_dir(), self.fname)
            dl.download()

        return SPKKernel(local_path)


class RemoteKernelsBase(abc.ABC):
    def __init_subclass__(cls):
        registry._kernels[cls.body][cls.type] = cls()
        assert cls.type in ['predict', 'recon']

    def get_latest_kernel(self):
        """
        Get the latest version of the kernel. If not present locally, will
        be downloaded.

        Returns
        -------
        astrospice.SPKKernel
        """
        kernels = self.get_remote_kernels()
        k = sorted(kernels)[-1]
        return k.fetch()

    def get_kernels(self, *, version=None):
        """
        Get a set of kernels. Any kernels not present locally will be
        downloaded.

        Parameters
        ----------
        version : int, optional
            If given, get only this version of the kernel.
        trange : tuple[astropy.time.Time], optional
            If given, only get kernels to cover the given time range.

        Returns
        -------
        list[astrospice.SPKKernel]
            List of kernels.

        Raises
        ------
        ValueError
            If there are no kernels available for the given type, version, and
            timerange.
        """
        kernels = self.get_remote_kernels()
        if version is not None:
            kernels = [k for k in kernels if k.version == version]

        if len(kernels) == 0:
            msg = f'No kernels available for {self.body}, type={self.type}'
            if version is not None:
                msg += f', version={version}'
            raise ValueError(msg)

        if self.type == 'predict':
            # Only get the most recent version
            kernels = [max(kernels)]
        dl = parfive.Downloader()
        for k in kernels:
            dl.enqueue_file(k.url, get_cache_dir(), k.fname)

        result = dl.download()
        return [SPKKernel(f) for f in result.data]

    @abc.abstractmethod
    def get_remote_kernels(self):
        """
        Get a list of all available remote kernels.

        Returns
        -------
        list[RemoteKernel]
        """
