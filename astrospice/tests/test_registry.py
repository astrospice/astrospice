import pytest
from astropy.table import Table

from astrospice import Body, SPKKernel, registry

# Ignore dubious year warnings for years a while in the future
pytestmark = pytest.mark.filterwarnings(r'ignore:ERFA function.*dubious year')


@pytest.mark.parametrize('body', registry.bodies)
def test_search(body):
    kernels = registry.get_available_kernels(body)
    assert isinstance(kernels, Table)


def test_get_latest():
    kernel = registry.get_latest_kernel('psp', 'predict')
    assert isinstance(kernel, SPKKernel)
    assert kernel.bodies == [Body('SOLAR PROBE PLUS')]
