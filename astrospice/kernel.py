from pathlib import Path

import spiceypy
from astropy.time import Time

from astrospice.body import Body

__all__ = ['KernelBase', 'SPKKernel']


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

    @property
    def fname(self):
        """Path to kernel file."""
        return Path(self._fname)

    @property
    def _fname_str(self):
        return str(self.fname)


class SPKKernel(KernelBase):
    """
    A class for a single .spk kernel.

    References
    ----------
    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/spk.html
    """
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
