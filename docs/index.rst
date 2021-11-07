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
  <Table length=4>
  Mission   Type  Version        Start time               End time
    str3    str7   int64            Time                    Time
  ------- ------- ------- ----------------------- -----------------------
      psp predict      38 2018-08-12 00:00:00.000 2025-08-31 00:00:00.000
      psp predict      37 2018-08-12 00:00:00.000 2025-08-31 00:00:00.000
      psp predict      36 2018-08-12 00:00:00.000 2025-08-31 00:00:00.000
      psp predict      35 2018-08-12 00:00:00.000 2025-08-31 00:00:00.000


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
