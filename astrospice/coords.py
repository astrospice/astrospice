from functools import wraps

import astropy.units as u
import numpy as np
import spiceypy
from astropy.coordinates import SkyCoord
from astropy.coordinates.solar_system import solar_system_ephemeris
from astropy.time import Time

from astrospice.body import Body

__all__ = ['generate_coords']


def use_astropy_ephem(outer):
    @wraps(outer)
    def inner(*args, **kwargs):
        # If
        ephem = solar_system_ephemeris.get()
        known_ephem = ['de430', 'de432s', 'de440', 'de440s']
        if ephem not in known_ephem:
            ephem = 'de440s'
        kernel = solar_system_ephemeris.get_kernel(ephem)
        spiceypy.furnsh(kernel.daf.file.name)

        result = outer(*args, **kwargs)
        return result
    return inner


@use_astropy_ephem
def generate_coords(body, times):
    """
    Generate coordinates.

    Returns
    -------
    `~astropy.coordinates.SkyCoord`
    """
    body = Body(body)
    times_et = np.atleast_1d(Time(times).et)
    # Spice needs a funny set of times
    abcorr = str(None)
    frame = 'J2000'

    # Do the calculation
    pos_vel, lightTimes = spiceypy.spkezr(
        body.name, times_et, frame, abcorr,
        'SOLAR SYSTEM BARYCENTER')

    positions = np.array(pos_vel)[:, :3] * u.km
    velocities = np.array(pos_vel)[:, 3:] * u.km / u.s

    return SkyCoord(x=positions[:, 0],
                    y=positions[:, 1],
                    z=positions[:, 2], frame='icrs',
                    representation_type='cartesian')
