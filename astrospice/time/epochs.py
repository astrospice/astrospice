from astropy.time.formats import TimeFromEpoch, erfa

__all__ = ['ETEpoch']


class ETEpoch(TimeFromEpoch):
    """
    Seconds from 12 noon, Jan 1st 2000. This is the epoch that SPICE uses
    internally.

    References
    ----------
    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/time.html#The%20J2000%20Epoch
    """
    name = 'et'
    unit = 1.0 / erfa.DAYSEC  # Seconds
    epoch_val = '2000-01-01 12:00:00'
    epoch_val2 = None
    epoch_scale = 'tdb'
    epoch_format = 'iso'
