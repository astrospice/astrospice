import pytest

import astrospice.registry as spice_reg


@pytest.mark.parametrize('name', spice_reg.names)
@pytest.mark.parametrize('type', ['predict', 'recon'])
def test_searches(name, type):
    if type not in spice_reg[name]:
        pytest.skip(f'{name} has no entry for type "{type}"')
    spice_reg.get_remote_kernels(name, type)
