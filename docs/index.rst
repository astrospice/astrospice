astrospice Documentation
------------------------

This is the documentation for astrospice.

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Using the kernel registry
=========================
``astrospice`` has a built in registry of kernels. Lets start by loading the
registry::

  >>> from astrospice import registry


The available missions can be seen by printing the registry::

  >>> print(registry)
  Known kernels: ['psp']

Available kernels for individual missions can be queried using `get_available_kernels`::

  >>> registry.get_available_kernels('psp')
  <Table length=20>
  Mission   Type  Version        Start time               End time
    str3    str7   int64            Time                    Time
  ------- ------- ------- ----------------------- -----------------------
      psp predict      38 2018-08-12 00:00:00.000 2025-08-31 00:00:00.000
      psp predict      37 2018-08-12 00:00:00.000 2025-08-31 00:00:00.000
      psp predict      36 2018-08-12 00:00:00.000 2025-08-31 00:00:00.000
      psp predict      35 2018-08-12 00:00:00.000 2025-08-31 00:00:00.000
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


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
