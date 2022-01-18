import pytest

from astrospice import Kernel


def test_unkown_extension(tmp_path):
    fpath = tmp_path / 'test.xyz'
    with pytest.raises(ValueError, match='Filename extension ".xyz" not in'):
        Kernel(fpath)
