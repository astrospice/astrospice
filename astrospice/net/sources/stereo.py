from urllib.request import urlopen
from bs4 import BeautifulSoup

from astropy.time import Time
import numpy as np

from astrospice.net import RemoteKernelsBase, RemoteKernel


__all__ = ['STEREORecon']


stereo_url = 'https://sohowww.nascom.nasa.gov/solarsoft/stereo/gen/data/spice'


class STEREORecon:
    type = 'recon'

    def get_remote_kernels(self):
        """
        Returns
        -------
        list[RemoteKernel]
        """
        page = urlopen(f'{stereo_url}/depm/{self.spacecraft}/')
        soup = BeautifulSoup(page, 'html.parser')

        kernel_urls = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href is not None and href.endswith('.bsp'):
                fname = href
                matches = self.matches(fname)
                if matches:
                    kernel_urls.append(
                        RemoteKernel(f'https://sppgway.jhuapl.edu/{href}',
                                     *matches[1:]))

        for k1, k2 in zip(kernel_urls[:-1], kernel_urls[1:]):
            k1.end_time = k2.start_time

        for k in kernel_urls:
            k.format = 'iso'
        return kernel_urls

    def matches(self, fname):
        """
        Check if the given filename matches the pattern of this kernel.

        Returns
        -------
        matches : bool
        start_time : astropy.time.Time
        end_time : astropy.time.Time
        version : int
        """
        # Example filename: ahead_2006_350_01.depm.bsp
        fname = fname.split('_')
        if (len(fname) != 4 or
                fname[0] != self.spacecraft):
            return False

        start_time = Time.strptime(fname[1] + fname[2], '%Y%j')
        end_time = None
        version = int(fname[3].split('.')[0])
        return True, start_time, end_time, version


class STEREOReconAhead(STEREORecon, RemoteKernelsBase):
    name = 'stereo-a'
    spacecraft = 'ahead'


class STEREOReconBehind(STEREORecon, RemoteKernelsBase):
    name = 'stereo-b'
    spacecraft = 'behind'
