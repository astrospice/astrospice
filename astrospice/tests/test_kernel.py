from pathlib import Path

import pytest
from spiceypy.utils.exceptions import SpiceFILEREADFAILED, SpiceNOSUCHFILE

from astrospice import Kernel
from astrospice.kernel import MetaKernel

# mimic text structure of MetaKernel
METAKERNEL_CONTENT = "KERNELS_TO_LOAD   = (\n                           '$KERNELS/test_subfolder/test_kernel.bsp'\n                         )"


@pytest.fixture()
def example_mk(tmp_path):
    fname = tmp_path / "temp_mk.tm"
    fname.write_text(METAKERNEL_CONTENT)
    return fname


def create_example_kernel(tmp_path):
    extra_kernel = tmp_path / 'test_subfolder' / 'test_kernel.bsp'
    extra_kernel.parent.mkdir()
    extra_kernel.write_text(" ")
    return extra_kernel


def test_unkown_extension(tmp_path):
    fpath = tmp_path / 'test.xyz'

    with pytest.raises(SpiceNOSUCHFILE):
        Kernel(fpath)


def test_metakernel_kernels(example_mk):
    mk = MetaKernel(example_mk)
    kernels = mk.kernels
    assert isinstance(kernels, list)
    assert isinstance(kernels[0], Path)
    assert kernels[0].name == "test_kernel.bsp"
    assert kernels[0].parent.stem == 'test_subfolder'


def test_all_kernels_exist(example_mk, tmp_path):
    mk = MetaKernel(example_mk)
    assert not mk.all_kernels_exist
    create_example_kernel(tmp_path)
    assert mk.all_kernels_exist


def test_metakernels_load(example_mk, tmp_path):
    mk = MetaKernel(example_mk)
    create_example_kernel(tmp_path)
    # should get a SpiceFILEREADFAILED error
    with pytest.raises(SpiceFILEREADFAILED):
        mk.load_kernels()


def test_metakernels_init(example_mk, tmp_path):
    create_example_kernel(tmp_path)
    with pytest.raises(SpiceFILEREADFAILED):
        MetaKernel(example_mk)
