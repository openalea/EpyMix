import numpy as np
from .data import meteo_path

### FUNCTION
# Define rainfall scenario (unfavorable, average, favorable) for septoria form rainfall data

### PARAMETERS
# years: which years from rainfall data
# delta_t: time step in dd

def f_rain(years, delta_t):
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
