Changelog
=========

0.2.0
-----
New features
~~~~~~~~~~~~
- Added `astrospice.MetaKernel` for interacting with meta kernel files. See
  the API documentation for info on helpful methods/properties.
- Added `astrospice.Kernel`, which can be used as a generic function to load
  kernels. Currently only SPK and MK files are supported natively by
  astrospice, but if a different (but valid) kernel type is passed SPICE
  will still be furnished with the kernel.
- Added Cassini to the kernel registry.

0.1.0
-----
First release of astrospice.
