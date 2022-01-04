import astrospice
import spiceypy
import astropy.units as u
from astropy.coordinates import SkyCoord, cartesian_to_spherical, Longitude
from astropy.time import Time
import numpy as np
from sunpy.coordinates import HeliographicCarrington
from sunpy.map import make_fitswcs_header
from astropy.wcs import WCS
import matplotlib.pyplot as plt


spiceypy.furnsh('solo_ANC_soc-eui-ik_V01.ti')
spiceypy.furnsh('solo_ANC_soc-sc-fk_V08.tf')
spiceypy.furnsh('solo_ANC_soc-sclk_20211204_V01.tsc')
spiceypy.furnsh('solo_ANC_soc-flown-att_20201119T082309-20201120T003115_V01.bc')
spiceypy.furnsh('solo_ANC_soc-eui-fsi-ck_20180930-21000101_V02.bc')
spiceypy.furnsh('naif0012.tls')
spiceypy.furnsh('solo_ANC_soc-sc-fof-ck_20180930-21000101_V02.bc')
spiceypy.furnsh('solo_ANC_soc-sci-fk_V07.tf')
spiceypy.furnsh('pck00010.tpc')
astrospice.registry.get_kernels('solar orbiter', 'predict')

shape, frame, boresight, n_vec, vec = spiceypy.getfov(-144210, room=100)

t = Time('2020-11-19 14:11:15')

R = spiceypy.pxform(frame, 'SOLO_SOLAR_MHP', t.et)
vec = np.dot(R, vec.T).T
orbiter_pos, lt = spiceypy.spkpos('SOLAR ORBITER', t.et,
                                  'IAU_SUN', 'LT', 'Sun')

frame = HeliographicCarrington(observer='self', obstime=t)
orbiter_coord = SkyCoord(x=orbiter_pos[0] * u.m,
                         y=orbiter_pos[1] * u.m,
                         z=orbiter_pos[2] * u.m,
                         representation_type='cartesian',
                         frame=frame)
orbiter_coord.representation_type = 'spherical'

n = 10**5
wcs = make_fitswcs_header([n, n],
                          SkyCoord(0*u.deg, 0*u.deg, observer=orbiter_coord,
                                   obstime=t,
                                   frame='helioprojective'),
                          reference_pixel=[n / 2, n / 2] * u.pix)
wcs.pop('rsun_obs')

dist, lat, lon = cartesian_to_spherical(vec[:, 2], vec[:, 0], vec[:, 1])
lon = Longitude(lon, wrap_angle=np.pi*u.rad)
eui_coords = SkyCoord(lon, lat, observer=orbiter_coord, frame='helioprojective')
print(eui_coords)
print(WCS(wcs).world_to_pixel(eui_coords))

fig = plt.figure()
ax = fig.add_subplot(111, projection=WCS(wcs))
ax.plot_coord(eui_coords, marker='o')
ax.set_xlim(0, n)
ax.set_ylim(0, n)
plt.show()
