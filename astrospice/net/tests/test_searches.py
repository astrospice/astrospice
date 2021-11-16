import pytest
from astropy.table import Table

from astrospice import registry as spice_reg


@pytest.mark.parametrize('body', spice_reg.bodies)
def test_search(body):
    kernels = spice_reg.get_available_kernels(body)
    assert isinstance(kernels, Table)
