import pytest
from astropy.table import Table

from astrospice import registry


@pytest.mark.parametrize('body', registry.bodies)
def test_search(body):
    kernels = registry.get_available_kernels(body)
    assert isinstance(kernels, Table)
