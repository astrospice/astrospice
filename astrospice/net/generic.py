from dataclasses import dataclass

from astropy.coordinates.solar_system import solar_system_ephemeris
from astropy.utils.data import download_file
import spiceypy

from astrospice.config import get_cache_dir


_known_jpl_ephem = ['de430', 'de432s', 'de440', 'de440s']
_ephem_name = solar_system_ephemeris.get()
if _ephem_name not in _known_jpl_ephem:
    _ephem_name = 'de440s'

_ephem_url = ('https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/'
              f'planets/{_ephem_name}.bsp')

_generic_files = [
    'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk',
    _ephem_url
]


def _setup_generic_files():
    for url in _generic_files:
        spiceypy.furnsh(download_file(url, cache=True))

    return _ephem_name
