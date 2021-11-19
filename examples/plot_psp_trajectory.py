"""
Parker Solar Probe trajectory
=============================

In this example we compute and plot the trajectory of Parker Solar Probe across
it's nominal mission phase.
"""
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from astropy.time import Time, TimeDelta
from astropy.visualization import quantity_support
from sunpy.coordinates import HeliocentricInertial

import astrospice

# Enable support for plotting astropy Quantities.
quantity_support()

###############################################################################
# First we'll get the Parker Solar Probe SPICE kernel. To get the trajectory
# in the future choose the 'predict' option, which will give us a kernel for
# the predicted trajectory.
#
# We then inspect the kernel, to check it's time coverage.
kernels = astrospice.registry.get_kernels('psp', 'predict')
psp_kernel = kernels[0]
coverage = psp_kernel.coverage('SOLAR PROBE PLUS')
print(coverage.iso)

###############################################################################
# To generate some coordinates we do not need the kernel object as astrospice
# automatically registers the kernel with SPICE when ``get_kernels`` was called
# above.
dt = TimeDelta(0.5 * u.day)
times = Time(np.arange(coverage[0], Time('2022-01-01'), dt))
coords = astrospice.generate_coords('SOLAR PROBE PLUS', times)
print(coords[0:4])

###############################################################################
# Note that the coordinates are generated in the ICRS coordinate system. To
# change this to a more useful heliocentric coordinate system we can use
# sunpy's built in Heliographic Carrington coordinate frame.
new_frame = HeliocentricInertial()
coords = coords.transform_to(new_frame)
print(coords[0:4])

###############################################################################
# Now we can plot the coordinates in this new coordinate system
fig = plt.figure()
ax = fig.add_subplot(projection='polar')
ax.scatter(coords.lon.to(u.rad), coords.distance.to(u.au), c=times.jd, s=2)
plt.show()
