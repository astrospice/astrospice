
import spiceypy
from astropy.coordinates.solar_system import solar_system_ephemeris
from astropy.utils.data import download_file

__all__ = ['set_solar_system_ephem', 'get_solar_system_ephem']

_known_jpl_ephem = ['de430', 'de432s', 'de440', 'de440s']
_jpl_ephem = solar_system_ephemeris.get()
if _jpl_ephem not in _known_jpl_ephem:
    _jpl_ephem = 'de440s'

_generic_files = [
    'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk',
]


def set_solar_system_ephem(name):
    """
    Set a JPL solar system ephemeris file. This will be downloaded and then
    cached for subsequent calls, and loaded into SPICE.

    Parameters
    ----------
    name : str
        Ephemeris name. Can be any ephemeris filename present at
        https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/
    """
    url = ('https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/'
           f'planets/{name}.bsp')
    fname = download_file(url, cache=True)
    spiceypy.furnsh(fname)

    global _jpl_ephem
    _jpl_ephem = name


def get_solar_system_ephem():
    """
    Get the currently set JPL solar system ephemeris file.

    Returns
    -------
    name : str
        Ephemeris name.
    """
    global _jpl_ephem
    return _jpl_ephem


def _setup_generic_files():
    for url in _generic_files:
        spiceypy.furnsh(download_file(url, cache=True))

    global _jpl_ephem
    set_solar_system_ephem(_jpl_ephem)
