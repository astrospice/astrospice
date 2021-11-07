"""
`astrospice.registry`
---------------------
A registry of SPICE kernels for various missions.
"""
from collections import defaultdict
from dataclasses import dataclass
import pathlib

from astropy.table import Table, vstack
from astropy.time import Time
import parfive

kernel_dir = pathlib.Path('/Users/dstansby/Data/spice')


class KernelRegistry:
    def __init__(self):
        self._kernels = defaultdict(dict)

    def __str__(self):
        return f'Known kernels: {self.names}'

    def __getitem__(self, idx):
        return self._kernels[idx]

    @property
    def names(self):
        """
        Names of the available kernels.
        """
        return list(self._kernels.keys())

    def check_name(self, name):
        """
        Raise an error if ``name`` isn't in the registry.
        """
        if name not in self.names:
            raise ValueError(
                f'{name} not in list of registered names: {self.names}')

    def get_available_kernels(self, name):
        """
        Get all the available kernels.

        Parameters
        ----------
        name : str
        type : str

        Returns
        -------
        astropy.table.Table
        """
        tables = []
        for type in self._kernels[name]:
            kernels = self._kernels[name][type].get_remote_kernels()
            urls = [k.url for k in kernels]
            stimes = [k.start_time for k in kernels]
            etimes = [k.end_time for k in kernels]
            versions = [k.version for k in kernels]
            tables.append(Table({'Mission': [name] * len(urls),
                                 'Type': [type] * len(urls),
                                 'Version': versions,
                                 'Start time': stimes,
                                 'End time': etimes}))

        tables = vstack(tables)
        tables['Start time'].format = 'iso'
        tables['End time'].format = 'iso'
        return tables

    def get_latest_kernel(self, name, type):
        self.check_name(name)
        return self._kernels[name][type].get_latest_kernel()

    def get_kernels(self, name, type, *, trange=None):
        """
        Get a set of kernels. Any kernels not present locally will be
        downloaded.

        Parameters
        ----------
        name : str
            Spacecraft name.
        type : str
            ``'recon'`` or ``'pred'`` to downloaded reconstructed or predicted
            kernels respectively.
        trange : tuple[Time], optional
            If given, only get kernels to cover the given time range.

        Returns
        -------
        list[Path]
            List of local filepaths.
        """
        self.check_name(name)
        return self._kernels[name][type].get_kernels(type, trange=trange)


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

    @property
    def fname(self):
        return self.url.split('/')[-1]

    def fetch(self):
        """
        Get the kernel. If not present locally, will be downloaded.
        """
        local_path = kernel_dir / self.fname
        if not local_path.exists():
            dl = parfive.Downloader()
            dl.enqueue_file(self.url, kernel_dir, self.fname)
            dl.download()

        return local_path


class RemoteKernelsBase:
    def __init_subclass__(cls):
        registry._kernels[cls.name][cls.type] = cls()
        assert cls.type in ['predict', 'recon']

    def get_latest_kernel(self):
        """
        Get the latest version of the kernel. If not present locally, will
        be downloaded.

        Returns
        -------
        kernel_path : pathlib.Path
            Path to the local kernel file.
        """
        kernels = self.get_remote_kernels()
        k = sorted(kernels)[-1]
        return k.fetch()

    def get_kernels(self, type, *):
        """
        Get a set of kernels. Any kernels not present locally will be
        downloaded.

        Parameters
        ----------
        type : str
            ``'recon'`` or ``'pred'`` to downloaded reconstructed or predicted
            kernels respectively.
        trange : tuple[Time], optional
            If given, only get kernels to cover the given time range.

        Returns
        -------
        list[Path]
            List of local filepaths.
        """
        kernels = self.get_remote_kernels()
        if type == 'predict':
            kernels = [max(kernels)]
        dl = parfive.Downloader()
        for k in kernels:
            dl.enqueue_file(k.url, kernel_dir, k.fname)

        result = dl.download()
        return result.data
