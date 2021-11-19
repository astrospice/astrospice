
import astropy.units as u
import numpy as np
import spiceypy
from astropy.coordinates import SkyCoord
from astropy.time import Time

from astrospice.body import Body

__all__ = ['generate_coords']


def generate_coords(body, times):
    """
    Generate coordinates.

    Returns
    -------
    `~astropy.coordinates.SkyCoord`
    """
    body = Body(body)
    times = Time(times)
    times_et = np.atleast_1d(times.et)
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
                    z=positions[:, 2],
                    obstime=times,
                    frame='icrs',
                    representation_type='cartesian')
