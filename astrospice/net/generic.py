from dataclasses import dataclass

import parfive
import spiceypy

from astrospice.config import get_cache_dir


@dataclass
class GenericFile:
    fname: str
    url: str

    @property
    def local_path(self):
        return get_cache_dir() / self.fname

    def fetch(self):
        if not self.local_path.exists():
            dl = parfive.Downloader()
            dl.enqueue_file(f'{self.url}/{self.fname}', get_cache_dir(), self.fname)
            dl.download()

        return self.local_path


lsk = GenericFile(
    'naif0012.tls',
    'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk')


def _setup_generic_files():
    for k in [lsk]:
        spiceypy.furnsh(str(k.fetch()))
