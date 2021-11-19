from packaging import version

import astropy
import astropy.units as u
import hypothesis.strategies as st
import pytest
from astropy.coordinates import get_body
from astropy.tests.helper import assert_quantity_allclose
from astropy.time import Time
from hypothesis import given, settings

import astrospice
from astrospice import generate_coords


@st.composite
def times(draw, min_time='1960-01-01', max_time='2024-01-01'):
    days = st.floats(min_value=0,
                     max_value=(Time(max_time) - Time(min_time)).to(u.day).value,
                     allow_nan=False, allow_infinity=False)
    return Time(min_time) + draw(days) * u.day


@pytest.mark.parametrize('ephem', ['de432s', 'de440s'])
@settings(max_examples=100, deadline=None)
@given(time=times())
def test_against_horizons(time, ephem):
    if (ephem == 'de440s' and
            (version.parse(astropy.__version__) < version.parse('4.3'))):
        pytest.mark.skip('de440s ephemeris only available in astropy>=4.3')

    body = 'Earth'
    astrospice.set_solar_system_ephem(ephem)
    horizons_coord = get_body(body, time, ephemeris=ephem)
    astrospice_coord = generate_coords(body, time)
    assert_quantity_allclose(horizons_coord.separation_3d(astrospice_coord),
                             0*u.km, atol=50*u.m)


def test_different_ephem():
    # Check that setting a different ephemeris has an effect
    coords = []
    body = 'Earth'
    time = Time('2020-01-01')
    for ephem in ['de432s', 'de440s']:
        astrospice.set_solar_system_ephem(ephem)
        coords.append(generate_coords(body, time))

    # Check that generated coordinates are different
    assert coords[0].separation_3d(coords[1]) > 100 * u.m
