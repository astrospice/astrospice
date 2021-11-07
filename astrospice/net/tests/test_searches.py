import pytest

from astrospice import registry as spice_reg
from astrospice.net import RemoteKernel


@pytest.mark.parametrize('name', spice_reg.names)
@pytest.mark.parametrize('type', ['predict', 'recon'])
def test_searches(name, type):
    if type not in spice_reg[name]:
        pytest.skip(f'{name} has no registry entry for type {type}')

    kernels = spice_reg.get_remote_kernels(name, type)
    assert isinstance(kernels, list)
    for k in kernels:
        assert isinstance(k, RemoteKernel)
