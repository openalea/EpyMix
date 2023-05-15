import numpy as np
from .data import meteo_path

def rain(year, n_season, delta_t):
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
    years = np.arange(year,year+n_season,1) #1995: bad; 1997: medium, 2000: good
    years = years.tolist()

    if not isinstance(years, list):
        years = [years]
    maxLa = 0
    rain=[]
    for year in years:
        path = meteo_path(year)
        with open(path) as f:
            a = f.read().splitlines()
            a = np.array([int(v) for v in a])
            A = -100 * np.ones((1000))
            A[0:len(a)] = a
            rain = np.append(rain,A)
            maxLa = max(maxLa, len(a))
    rain = rain.reshape([len(A), len(years)], order='F')
    rain = np.ceil(rain[0:maxLa]/int(delta_t))
    return rain
