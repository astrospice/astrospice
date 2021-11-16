from astropy.time.formats import TimeFromEpoch, erfa


class ETEpoch(TimeFromEpoch):
    """
    Seconds from 12 noon, Jan 1st 2000. This is the epoch that SPICE uses
    internally.
    """
    name = 'et'
    unit = 1.0 / erfa.DAYSEC  # Seconds
    epoch_val = '2000-01-01 12:00:00'
    epoch_val2 = None
    epoch_scale = 'tdb'
    epoch_format = 'iso'
