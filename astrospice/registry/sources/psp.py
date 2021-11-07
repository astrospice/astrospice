from urllib.request import urlopen
from bs4 import BeautifulSoup

from astropy.time import Time

from astrospice.registry import RemoteKernelsBase


__all__ = ['PSPPredicted']


class PSPPredicted(RemoteKernelsBase):
    name = 'psp'
    type = 'predict'

    def get_remote_links():
        page = urlopen('https://sppgway.jhuapl.edu/lpredict_ephem')
        soup = BeautifulSoup(page, 'html.parser')

        kernel_urls = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href is not None and href.startswith('/MOC/ephemerides//'):
                kernel_urls.append(f'https://sppgway.jhuapl.edu/{href}')

        return kernel_urls

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
        # Example filename: spp_nom_20180812_20250831_v038_RO5.bsp
        fname = fname.split('_')
        if (len(fname) != 6 or
                fname[0] != 'spp' or
                fname[1] != 'nom'):
            return False

        start_time = Time.strptime(fname[2], '%Y%m%d')
        end_time = Time.strptime(fname[3], '%Y%m%d')
        version = int(fname[4][1:])
        return True, start_time, end_time, version
