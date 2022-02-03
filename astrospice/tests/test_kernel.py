from pathlib import Path

import pytest
from spiceypy.utils.exceptions import SpiceFILEREADERROR

from astrospice import Kernel
from astrospice.kernel import MetaKernel

# mimic text structure of MetaKernel
METAKERNEL_CONTENT = "KERNELS_TO_LOAD   = (\n                           '$KERNELS/test_subfolder/test_kernel.bsp'\n                         )"


def test_unkown_extension(tmp_path):
    fpath = tmp_path / 'test.xyz'
    with pytest.raises(ValueError, match='Filename extension ".xyz" not in'):
        Kernel(fpath)


def test_metakernel_kernels(tmp_path):
    fname = tmp_path / "temp_mk.tm"
    fname.write_text(METAKERNEL_CONTENT)
    mk = MetaKernel(fname)
    kernels = mk.kernels
    assert isinstance(kernels, list)
    assert isinstance(kernels[0], Path)
    assert kernels[0].name == "test_kernel.bsp"
    assert kernels[0].parent.stem == 'test_subfolder'


def test_kernels_exist(tmp_path):
    fname = tmp_path / "temp_mk.tm"
    fname.write_text(METAKERNEL_CONTENT)
    mk = MetaKernel(fname)
    assert not mk.kernels_exist
    # now add the file and check
    extra_kernel = tmp_path / 'test_subfolder' / 'test_kernel.bsp'
    extra_kernel.parent.mkdir()
    extra_kernel.write_text(" ")
    assert mk.kernels_exist


def test_metakernels_load(tmp_path):
    fname = tmp_path / "temp_mk.tm"
    fname.write_text(METAKERNEL_CONTENT)
    mk = MetaKernel(fname)
    extra_kernel = tmp_path / 'test_subfolder' / 'test_kernel.bsp'
    extra_kernel.parent.mkdir()
    extra_kernel.write_text(" ")
    # should get a SpiceFILEREADFAILED error
    with pytest.raises(Exception) as exc:
        mk.load_kernels()
        assert isinstance(exc.value, SpiceFILEREADERROR)
