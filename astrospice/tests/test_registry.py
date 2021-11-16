import pytest
from astropy.table import Table

from astrospice import registry


@pytest.mark.parametrize('body', registry.bodies)
def test_search(body):
    if 'st' in body:
        pytest.xfail('STEREO servers not working')
    kernels = registry.get_available_kernels(body)
    assert isinstance(kernels, Table)
