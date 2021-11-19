Guided walkthrough
==================

Finding kernels
---------------

Using the kernel registry
~~~~~~~~~~~~~~~~~~~~~~~~~
``astrospice`` has a built in registry of kernels. Lets start by loading the
registry::

  >>> import astrospice

The available bodies can be seen by printing the registry::

  >>> print(astrospice.registry)
  Known kernels: ['psp', 'solar orbiter', 'stereo-a', 'stereo-b']

Available kernels for individual bodies can be queried using
:meth:`~astrospice.net.KernelRegistry.get_available_kernels`::

  >>> astrospice.registry.get_available_kernels('psp')
  <Table length=...>
  Mission   Type  Version        Start time               End time
  ...
  ------- ------- ------- ----------------------- -----------------------
  ...
      psp predict      38 2018-08-12 00:00:00.000 2025-08-31 00:00:00.000
      psp predict      37 2018-08-12 00:00:00.000 2025-08-31 00:00:00.000
      psp predict      36 2018-08-12 00:00:00.000 2025-08-31 00:00:00.000
      psp predict      35 2018-08-12 00:00:00.000 2025-08-31 00:00:00.000
  ...
      psp   recon       1 2021-07-23 00:00:00.000 2021-09-04 00:00:00.000
      psp   recon       1 2021-05-24 00:00:00.000 2021-07-23 00:00:00.000
      psp   recon       1 2021-03-25 00:00:00.000 2021-05-25 00:00:00.000
      psp   recon       1 2021-02-26 00:00:00.000 2021-03-25 00:00:00.000
      psp   recon       1 2021-01-01 00:00:00.000 2021-02-26 00:00:00.000
      psp   recon       1 2020-10-16 00:00:00.000 2021-01-01 00:00:00.000
      psp   recon       1 2020-08-02 00:00:00.000 2020-10-16 00:00:00.000
      psp   recon       1 2020-07-05 00:00:00.000 2020-08-02 00:00:00.000
      psp   recon       1 2020-05-05 00:00:00.000 2020-07-05 00:00:00.000
      psp   recon       1 2020-03-01 00:00:00.000 2020-05-05 00:00:00.000
      psp   recon       1 2020-01-01 00:00:00.000 2020-03-01 00:00:00.000
      psp   recon       1 2019-09-14 00:00:00.000 2020-01-01 00:00:00.000
      psp   recon       1 2019-04-16 00:00:00.000 2019-09-14 00:00:00.000
      psp   recon       1 2019-01-20 00:00:00.000 2019-04-16 00:00:00.000
      psp   recon       1 2018-10-08 00:00:00.000 2019-01-20 00:00:00.000
      psp   recon       1 2018-08-12 00:00:00.000 2018-10-08 00:00:00.000

The first columns shows the queried body. The second columns shows the type
of kernel. This is either 'predict', for predicted ephemeris, or 'recon' for
reconstructed ephemeris. The third column shows the version (typically used
for updates to reconstructed kernels), and the last two columns show the
start and end times covered by each kernel, if known.

Downloading kernels
~~~~~~~~~~~~~~~~~~~
To download a set of kernels, use the ``.get_kernels()`` method::

  >>> kernels = astrospice.registry.get_kernels('psp', 'predict', version=35)

Kernels are downloaded to the astrospice cache directory. Note that in this
example a specific version of the kernel is downloaded to make the results
below reproducible. Omitting the ``version`` keyword argument will get the
latest version of the kernel.

Generating coordinates
----------------------
First, lets get a kernel::

  >>> k = kernels[0]
  >>> type(k)
  <class 'astrospice.kernel.SPKKernel'>
  >>> print(k)
  SPK Kernel for Solar probe plus

The `~astrospice.SPKKernel` object has some handy methods to determine which
bodies and date ranges the kernel covers::

  >>> k.bodies
  [Body(SOLAR PROBE PLUS)]
  >>> k.coverage('SOLAR PROBE PLUS').iso
  array(['2018-08-12 08:15:14.160', '2025-08-31 09:11:39.190'], dtype='<U23')

``get_kernels`` will automatically furnish SPICE with the kernels it finds, so
we don't need to worry about the kernel object any more.

To generate coordinates, use the ``generate_coords`` function::

  >>> from astropy.time import Time, TimeDelta
  >>> import astropy.units as u
  >>> import numpy as np
  >>>
  >>> t1, t2 = Time('2020-01-01'), Time('2021-01-01')
  >>> dt = TimeDelta(1*u.day)
  >>> times = np.arange(t1, t2, dt)
  >>> coords = astrospice.generate_coords('SOLAR PROBE PLUS', times)
  >>> coords
  <SkyCoord (ICRS): (x, y, z) in km
     [( 9.93695832e+07,   4692424.94313492, -4.22612507e+06),
      ( 9.74891722e+07,   6289300.87376746, -3.38866168e+06),
      ( 9.55063967e+07,   7880665.59182881, -2.54719992e+06),
  ...

The generated coordinates are in the ICRS coordinate system. To get them in
another system the astropy coordinates machinery can be used. Here we'll
transform them into a heliocentric coordinate system provided by sunpy::

  >>> from sunpy.coordinates import HeliographicCarrington
  >>> to_frame = HeliographicCarrington(observer='self')
  >>> coords_car = coords.transform_to(to_frame)
  >>> coords_car
  <SkyCoord (HeliographicCarrington: obstime=['2020-01-01 00:00:00.000' '2020-01-02 00:00:00.000'
   '2020-01-03 00:00:00.000' '2020-01-04 00:00:00.000'
   ...
   '2020-12-30 00:00:00.000' '2020-12-31 00:00:00.000'], rsun=695700.0 km, observer=self): (lon, lat, radius) in (deg, deg, km)
      [(332.12529441,  3.71079513, 1.00114385e+08),
       (319.00710685,  3.69055562, 9.82750254e+07),
       (305.93031377,  3.66817727, 9.63683478e+07),
       ...

Solar system ephemeris
~~~~~~~~~~~~~~~~~~~~~~
If a JPL ephemeris is set in astropy, astrospice will automatically use it. If
not, the 'de440s' ephemeris will be used by deafult. To set a different
ephemeris, use the :func:`astrospice.set_solar_system_ephem` function.
