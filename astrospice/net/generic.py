from dataclasses import dataclass

import parfive
import spiceypy

from .reg import kernel_dir


@dataclass
class GenericFile:
    fname: str
    url: str

    @property
    def local_path(self):
        return kernel_dir / self.fname

    def fetch(self):
        if not self.local_path.exists():
            dl = parfive.Downloader()
            dl.enqueue_file(f'{self.url}/{self.fname}', kernel_dir, self.fname)
            dl.download()[0]

        return self.local_path

lsk = GenericFile(
    'naif0012.tls',
    'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk')


def setup_generic_files():
    for k in [lsk]:
        spiceypy.furnsh(str(k.fetch()))
