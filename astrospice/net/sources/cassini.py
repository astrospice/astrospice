from urllib.request import urlopen

from astropy.time import Time
from bs4 import BeautifulSoup

from astrospice.net.reg import RemoteKernel, RemoteKernelsBase

__all__ = ['CassiniRecon']


class CassiniRecon(RemoteKernelsBase):
    body = 'cassini'
    type = 'recon'

    def get_remote_kernels(self):
        """
        Returns
        -------
        list[RemoteKernel]
        """
        base_url = 'https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk'
        page = urlopen(base_url)
        soup = BeautifulSoup(page, 'html.parser')

        kernel_urls = []
        for link in soup.find_all('a'):
            fname = link.get('href')
            if (fname is not None and fname.endswith('.bsp')):
                matches = self.matches(fname)
                if matches:
                    kernel_urls.append(RemoteKernel(
                        f'{base_url}/{fname}', *matches[1:]))

        return kernel_urls

    @staticmethod
    def matches(fname):
        """
        Check if the given filename matches the pattern of this kernel.

        Returns
        -------
        matches : bool
        start_time : astropy.time.Time
        end_time : astropy.time.Time
        version : int
        """
        # Example filename: 200128RU_SCPSE_09200_09215.bsp
        fname = fname.split('_')
        if (len(fname) != 4 or
                fname[0] != '200128RU' or
                fname[1] != 'SCPSE' or
                not fname[3].endswith('.bsp')):
            return False

        start_time = Time.strptime(fname[2], '%y%j')
        end_time = Time.strptime(fname[3].split('.')[0], '%y%j')
        version = 1
        return True, start_time, end_time, version
