Using meta-kernels
==================
Meta-kernels contain a collection of other kernels to either download or load into SPICE.
astrospice supports loading meta-kernels and using them to download and load their listed kernels into SPICE.

First lets manually download a meta-kernel for Solar Oribter::

  >>> from parfive import Downloader
  >>> filename = 'solo_ANC_soc-flown-mk_V105_20200414_001.tm'
  >>> Downloader.simple_download([f'http://spiftp.esac.esa.int/data/SPICE/SOLAR-ORBITER/kernels/mk/{filename}'], path='./')
  <parfive.results.Results object at ...>
  ['solo_ANC_soc-flown-mk_V105_20200414_001.tm']

Now we can load this using the `.Kernel` class::

  >>> from astrospice import Kernel
  >>> orbiter_mk = Kernel(filename)
  >>> print(orbiter_mk)
  MetaKernel('solo_ANC_soc-flown-mk_V105_20200414_001.tm')

The kernels stored in a meta-kernel can be inspected using the ``.kernels`` property::

  >>> print(len(orbiter_mk))
  82
  >>> print(orbiter_mk.kernels)
  [PosixPath('ck/solo_ANC_soc-sc-iboom-ck_20180930-21000101_V01.bc'), PosixPath('ck/solo_ANC_soc-sc-oboom-ck_20180930-21000101_V01.bc'), ...]

The output is truncated, but we can see that there are 82 kernels listed within this meta-kernel.
To check if all of these kernels are available locally, we can use the ``all_kernels_exist`` property::

  >>> print(orbiter_mk.all_kernels_exist)
  False
