This is the documentation for astrospice.

Finding kernels
===============

Using the kernel registry
-------------------------
``astrospice`` has a built in registry of kernels. Lets start by loading the
registry::

  >>> from astrospice import registry


The available bodies can be seen by printing the registry::

  >>> print(registry)
  Known kernels: ['psp', 'stereo-a', 'stereo-b']

Available kernels for individual bodies can be queried using `get_available_kernels`::

  >>> registry.get_available_kernels('psp')
  <Table length=21>
  Mission   Type  Version        Start time               End time
  ...
  ------- ------- ------- ----------------------- -----------------------
      psp predict      38 2018-08-12 00:00:00.000 2025-08-31 00:00:00.000
      psp predict      37 2018-08-12 00:00:00.000 2025-08-31 00:00:00.000
      psp predict      36 2018-08-12 00:00:00.000 2025-08-31 00:00:00.000
      psp predict      35 2018-08-12 00:00:00.000 2025-08-31 00:00:00.000
      psp   recon       1 2021-09-04 00:00:00.000 2021-11-04 00:00:00.000
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
-------------------
To download a set of kernels, use the ``.get_kernels()`` method::

  >>> kernels = registry.get_kernels('psp', 'predict')

Kernels are downloaded to the astrospice cache directory.

Generating coordinates
======================
First, lets get a kernel. ``get_kernels`` will automatically furnish SPICE with
the kernels it finds::

  >>> k = kernels[0]
  >>> type(k)
  <class 'astrospice.kernel.SPKKernel'>
  >>> print(k)
  SPK Kernel for Solar probe plus

The `SPKKernel` object has some handy methods to determine which bodies and
date ranges the kernel covers::

  >>> k.bodies
  [Body(SOLAR PROBE PLUS)]
  >>> k.coverage('SOLAR PROBE PLUS').iso
  array(['2018-08-12 08:15:14.160', '2025-08-31 13:05:00.950'], dtype='<U23')

Solar system ephemeris
----------------------
If a JPL ephemeris is set in astropy, astrospice will automatically use it. If
not, the 'de440s' ephemeris will be used by deafult. To set a different ephemeris,
see the astropy documentation.

API reference
=============

.. automodapi:: astrospice

.. automodapi:: astrospice.time
