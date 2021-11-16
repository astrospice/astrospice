Generating coordinates (`astropsice.coords`)
============================================


First, lets get a kernel. ``get_kernels`` will automatically furnish SPICE with
the kernels it finds::

  >>> from astrospice import registry
  >>> kernels = registry.get_kernels('psp', 'predict')
  >>> k = kernels[0]
  >>> type(k)
  SPKKernel
  >>> print(k)
  SPK Kernel for [Solar probe plus]

The `SPKKernel` object has some handy methods to determine which bodies and
date ranges the kernel covers::

  >>> k.bodies

  >>> k.coverage('SPP')

API reference
-------------

.. automodapi:: astrospice.coords
   :no-heading:
