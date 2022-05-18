from urllib.request import urlopen

from astropy.time import Time
from bs4 import BeautifulSoup

from astrospice.net.reg import RemoteKernel, RemoteKernelsBase

__all__ = ['PSPPredict', 'PSPRecon']


class PSPPredict(RemoteKernelsBase):
    body = 'psp'
    type = 'predict'

    def get_remote_kernels(self):
        """
        Returns
        -------
        list[RemoteKernel]
        """
        page = urlopen('https://spdf.gsfc.nasa.gov/pub/data/psp/ephemeris/spice/Long_Term_Predicted_Ephemeris/')
        soup = BeautifulSoup(page, 'html.parser')

        kernel_urls = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href is not None and href.startswith('spp'):
                fname = href.split('/')[-1]
                matches = self.matches(fname)
                if matches:
                    kernel_urls.append(
                        RemoteKernel(f'https://spdf.gsfc.nasa.gov/pub/data/psp/ephemeris/spice/Long_Term_Predicted_Ephemeris/{href}', *matches[1:]))

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


class PSPRecon(RemoteKernelsBase):
    body = 'psp'
    type = 'recon'

    def get_remote_kernels(self):
        """
        Returns
        -------
        list[RemoteKernel]
        """
        page = urlopen('https://sppgway.jhuapl.edu/recon_ephem')
        soup = BeautifulSoup(page, 'html.parser')

        kernel_urls = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if (href is not None and
                    href.startswith('MOC/reconstructed_ephemeris') and
                    'archive' not in href):
                fname = href.split('/')[-1]
                matches = self.matches(fname)
                if matches:
                    kernel_urls.append(
                        RemoteKernel(f'https://sppgway.jhuapl.edu/{href}',
                                     *matches[1:]))

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
        # Example filename: spp_recon_20180812_20181008_v001.bsp
        fname = fname.split('_')
        if (len(fname) != 5 or
                fname[0] != 'spp' or
                fname[1] != 'recon'):
            return False

        start_time = Time.strptime(fname[2], '%Y%m%d')
        end_time = Time.strptime(fname[3], '%Y%m%d')
        version = int(fname[4].split('.')[0][1:])
        return True, start_time, end_time, version
