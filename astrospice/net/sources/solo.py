from urllib.request import urlopen

from astropy.time import Time
from bs4 import BeautifulSoup

from astrospice.net.reg import RemoteKernel, RemoteKernelsBase

__all__ = ['SolarOrbiterPredict']


class SolarOrbiterPredict(RemoteKernelsBase):
    body = 'solar orbiter'
    type = 'predict'

    def get_remote_kernels(self):
        """
        Returns
        -------
        list[RemoteKernel]
        """
        base_url = 'http://spiftp.esac.esa.int/data/SPICE/SOLAR-ORBITER/kernels/spk'
        page = urlopen(base_url)
        soup = BeautifulSoup(page, 'html.parser')

        kernel_urls = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href is not None and href.endswith('.bsp'):
                fname = href.split('/')[-1]
                matches = self.matches(fname)
                if matches:
                    kernel_urls.append(
                        RemoteKernel(f'{base_url}/{fname}',
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
        # Example filename: spp_nom_20180812_20250831_v038_RO5.bsp
        fname = fname.split('_')
        if (len(fname) != 8 or
                fname[0] != 'solo' or
                fname[1] != 'ANC' or
                fname[2] != 'soc-orbit'):
            return False

        times = fname[3].split('-')
        start_time = Time.strptime(times[0], '%Y%m%d')
        end_time = Time.strptime(times[1], '%Y%m%d')
        version = int(fname[4][1:])
        return True, start_time, end_time, version
