import pytest

from astrospice import Body


def test_errors():
    with pytest.raises(ValueError, match='body must be an int or str'):
        Body([])

    with pytest.raises(ValueError, match='id "45869" not known by SPICE'):
        Body(45869)

    msg = 'Body name "not a body" not known by SPICE'
    with pytest.raises(ValueError, match=msg):
        Body('not a body')
