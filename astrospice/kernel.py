from pathlib import Path

import spiceypy
from astropy.time import Time

from astrospice.body import Body

__all__ = ['KernelBase', 'Kernel', 'SPKKernel']


# Mapping from filename extension to Kernel class
_REGISTRY = {}


class KernelBase:
    """
    Class for a single kernel.

    Notes
    -----
    When creating instances of this class, SPICE is automatically furnished
    with the kernel.
    """
    def __init__(self, fname):
        self._fname = fname
        spiceypy.furnsh(self._fname_str)

    def __init_subclass__(cls):
        _REGISTRY[cls._file_extension] = cls

    @property
    def fname(self):
        """Path to kernel file."""
        return Path(self._fname)

    @property
    def _fname_str(self):
        return str(self.fname)


def Kernel(fname):
    """
    Load a SPICE kernel.

    Parameters
    ----------
    fname : str, pathlib.Path
        Path to the kernel file.

    Returns
    -------
    kernel : KernelBase
    """
    extension = Path(fname).suffix
    if extension in _REGISTRY:
        return _REGISTRY[extension](fname)
    else:
        raise ValueError(f'Filename extension "{extension}" not in '
                         f'known extensions: {list(_REGISTRY.keys())}')


class SPKKernel(KernelBase):
    """
    A class for a single .spk kernel.

    References
    ----------
    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/spk.html
    """
    _file_extension = '.bsp'

    def __init__(self, fname):
        super().__init__(fname)
        # Run bodies() to validate the spice kernel
        self.bodies

    def __str__(self):
        body_strs = []
        for b in self.bodies:
            body_strs.append(f'{b.name.capitalize()}')
        body_strs = ', '.join(body_strs)
        return f'SPK Kernel for {body_strs}'

    @property
    def bodies(self):
        """List of the bodies stored within the kernel."""
        ids = [int(i) for i in spiceypy.spkobj(self._fname_str)]
        return [Body(i) for i in ids]

    def coverage(self, body):
        """
        The coverage window for a specified `Body`.

        Parameters
        ----------
        body

        Returns
        -------
        astropy.time.Time
        """
        body = Body(body)
        coverage = [t for t in spiceypy.spkcov(self._fname_str, body.id)]
        return Time(coverage, format='et').utc

class MetaKernel(KernelBase):
    """
    A class for a single .tm kernel.

    References
    ----------
    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/kernel.html#Additional%20Meta-kernel%20Specifications
    """
    _file_extension = '.tm'
    
    def __init__(self, fname):
        self._fname = fname
        self.change_path_value()
        if self.kernels_exist:
            self.load_kernels()
        else:
            print("Kernels are not yet loaded")
        
    def change_path_value(self):
        """
        Changes the PATH_VALUES parameter in the .tm file
        to point to the same folder as the .tm file.
        """
        #open the file
        with open(self.fname, 'r') as file:
            # read a list of lines into data
            data = file.readlines()

        #find the line with PATH_VALUES = ( '..' )
        for i, line in enumerate(data):
            line_split = line.split()
            if len(line_split) > 1 and line_split[0] == 'PATH_VALUES':
                if line_split[-2] == "'..'":
                    #replace the ".." with the folder path
                    data[i] = data[i].replace('..', str(self.fname.parent))
        
        #write over the original file
        with open(self.fname, 'w') as file:
            file.writelines( data )
            
    @property
    def kernels(self):
        "List of kernels specified by the metakernel"
        kernels = []
        with open(self.fname, "r") as file:
            look_for_kernels = False
            for  line in file:
                #split by whitespace
                line_split = line.split()
                
                # now find the ) bracket by itself, this is the end of kernels to load
                if len(line_split) >= 1 and line_split[0] == ')':
                    look_for_kernels = False
                    break
                
                if look_for_kernels == True and len(line_split) > 0:
                    # find the filename for the kernel. 
                    # The slicing removes the $KERNEL and the final '
                    kernel_fname = line_split[0][9:-1]
                    #do not add empty lines
                    if kernel_fname != '':
                        #slice removes the first \
                        kernels.append(kernel_fname[1:])
                
                if len(line_split) > 1 and line_split[0] == 'KERNELS_TO_LOAD':
                    look_for_kernels = True
        
        return kernels
    
    def load_kernels(self):
        """
        Loads the kernels specified by the metakernel
        """
        for kernel in self.kernels:
            try:
                Kernel(self.fname.parent / Path(kernel))
            except ValueError:
                print(f"Filetype {Path(kernel).suffix} not supported yet\n")
                
    def kernels_exist(self):
        """
        Checks if the kernels in the metakernel exist

        Returns
        -------
        Bool
            True if all kernels exist, False if not
        """
        for kernel in self.kernels:
            kernel_path = self.fname.parent / Path(kernel)
            if not kernel_path.exists:
                return False
        return True