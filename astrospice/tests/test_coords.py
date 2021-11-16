import astropy.units as u
import hypothesis.strategies as st
from astropy.coordinates import get_body
from astropy.tests.helper import assert_quantity_allclose
from astropy.time import Time
from hypothesis import given, settings

from astrospice import generate_coords


@st.composite
def times(draw, min_time='1960-01-01', max_time='2024-01-01'):
    days = st.floats(min_value=0,
                     max_value=(Time(max_time) - Time(min_time)).to(u.day).value,
                     allow_nan=False, allow_infinity=False)
    return Time(min_time) + draw(days) * u.day


@settings(max_examples=100)
@given(time=times())
def test_against_horizons(time):
    body = 'Earth'

    horizons_coord = get_body(body, time, ephemeris='de440s')
    astrospice_coord = generate_coords(body, time)
    assert_quantity_allclose(horizons_coord.separation_3d(astrospice_coord),
                             0*u.km, atol=50*u.m)
