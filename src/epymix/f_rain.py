import os
import numpy as np
import math
from epyland.data import meteo_path

#annees = [1994,1997]

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

from epyland.f_rain import f_rain
delta_t0 = 10 # constant, the model has been parameterise such as t = 10 degree-day
delta_t = 10 # time step
n_season2 = 24 # number of season
t2 = n_season2*250*int(delta_t0/delta_t)
season2 = 250*int(delta_t0/delta_t)  # 2500 dd %% length of a cropping season
annees2 = np.arange(1993,1993+n_season2,1)
annees2 = annees2.tolist()
rain2 = f_rain(annees2, delta_t)
pluie2 = []
for i in range (0, t2):
    pluie2.append(np.mod(i, season2) in rain2[:, np.mod(int(np.floor(i/season2)), rain2.shape[1])])
pluie3 = np.array(pluie2)
pluie3 = np.reshape(pluie2, (season2, n_season2), order='F')
pluie_sum = np.sum(pluie3, axis=0)
final = np.column_stack((annees2, pluie_sum))
final = final[np.argsort(final[:, 1])]