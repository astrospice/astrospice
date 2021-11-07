import pytest

from astropy.table import Table

from astrospice import registry as spice_reg
from astrospice.net import RemoteKernel


@pytest.mark.parametrize('name', spice_reg.names)
def test_search(name):
    kernels = spice_reg.get_available_kernels(name)
    assert isinstance(kernels, Table)
