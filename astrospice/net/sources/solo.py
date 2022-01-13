from urllib.request import urlopen

from astropy.time import Time
from bs4 import BeautifulSoup

from astrospice.net.reg import RemoteKernel, RemoteKernelsBase, MetaKernel

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

class SolarOrbiterMetakernel(RemoteKernelsBase):
    """Will load the metakernel and all the subsequent kernels listed.
    
    To start with I will just give it a local path to the metakernel.
    
    """
    
    body = 'solar orbiter'
    type = 'meta'
    
    def get_remote_kernels(self):
        #get the url of the remote meta kernel and download it
        """
        Returns
        -------
        list[RemoteKernel]
        """
        base_url = 'http://spiftp.esac.esa.int/data/SPICE/SOLAR-ORBITER/kernels/mk'
        page = urlopen(base_url)
        soup = BeautifulSoup(page, 'html.parser')

        kernel_urls = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href is not None and href.endswith('.tm'):
                fname = href.split('/')[-1]
                matches = self.matches(fname)
                if matches:
                    kernel_urls.append(
                        MetaKernel(f'{base_url}/{fname}', *matches[1:]))

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
        # Example filename: solo_ANC_soc-flown-mk_V106_20201216_001.tm
        fname = fname.split('_')
        if (len(fname) != 6 or
                fname[0] != 'solo' or
                fname[1] != 'ANC' or
                fname[2] != 'soc-flown-mk' and
                fname[2] != 'soc-pred-mk'):
            return False

        time = fname[4]
        time = Time.strptime(time, '%Y%m%d')
        version = int(fname[3][1:])
        return True, time, version

        
        #change the kernel attribute in the metakernel file
        
        #cycle through the listed files in the metakernel and download them
        
        #these have the same https address as the file system for my local copy
        #so save in this structure too
        
        #load as KernelBase objets
        
        #if .spk then load as one of those objects
        print('Downloading metakernel file')
    