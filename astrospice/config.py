from pathlib import Path

import astropy.config.paths

__all__ = ['get_cache_dir']


def get_cache_dir():
    """
    Get path to the astrospice cache directory.

    Returns
    -------
    cachedir : pathlib.Path
        The absolute path to the cache directory.
    """
    return Path(astropy.config.paths.get_cache_dir(rootname='astrospice'))
