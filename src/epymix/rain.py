import numpy as np
from .data import meteo_path

def rain(years, delta_t):
    """
    Define rainfall scenario.

    Define rainfall scenario (unfavorable, average, favorable) 
    for septoria form rainfall data

    Parameters
    ----------
    years: int
        which years from rainfall data
    delta_t: int
        time step in dd
    
    Returns
    -------
    numpy array
        rain
    """

    if not isinstance(years, list):
        years = [years]
    maxLa = 0
    _rain=[]
    for year in years:
        path = meteo_path(year)
        with open(path) as f:
            a = f.read().splitlines()
            a = np.array([int(v) for v in a])
            A = -100 * np.ones((1000))
            A[0:len(a)] = a
            _rain = np.append(_rain,A)
            maxLa = max(maxLa, len(a))
    _rain = _rain.reshape([len(A), len(years)], order='F')
    _rain = np.ceil(_rain[0:maxLa]/int(delta_t))
    return _rain
