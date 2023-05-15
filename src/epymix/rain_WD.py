import numpy as np
import pandas as pd
from .data import meteo_path

import pandas
pandas.set_option('display.max_colwidth', None)
import logging, sys
from weatherdata import WeatherDataHub

def rain(site, time_start, time_end, delta_t, sowing_date, rainfall_threshold):
    # years = np.arange(year, year + n_season, 1)
    # years = years.tolist()
    # if not isinstance(years, list):
    #     years = [years]

    maxLa = 0
    rain = []
    # for annee in years:
    ws = WeatherDataHub()
    meteo = ws.get_ressource(name=site)
    ds = meteo.data(parameters=[1002, 2001], stationId=[5],
                    timeStart=time_start, timeEnd=time_end,
                    timeZone='Europe/Paris', varname="id", usecache=True, savecache=True, display="ds")
    path = ds.to_dataframe()

    # Filtering by sowing date
    path.reset_index(inplace=True)
    path[['Date', 'Hour']] = path.time.astype(str).str.split(expand=True)
    path["Date"] = pd.to_datetime(path["Date"], dayfirst=False)
    path = path[(path['Date'] >= sowing_date)]

    # Calculatig degree-day
    path_max = path.groupby(path.columns[6])[path.columns[2]].max()
    path_min = path.groupby(path.columns[6])[path.columns[2]].min()
    t_base = 0
    degree_day_inc = [(((i + j) / 2) - t_base) for i, j in zip(path_max, path_min)]

    path_dd = path_max.reset_index()
    path_dd.drop(path_dd.columns[1], inplace=True, axis=1)
    path_dd['dd_inc'] = degree_day_inc
    path_dd["Date"] = pd.to_datetime(path_dd["Date"], dayfirst=True)
    path_dd.sort_values(by='Date', inplace=True)
    path_dd['dd_cum'] = path_dd['dd_inc'].cumsum()

    # Summing rainfall
    daily_rain = path.groupby(path.columns[6])[path.columns[3]].sum()
    daily_rain = daily_rain.reset_index()
    daily_rain["Date"] = pd.to_datetime(daily_rain["Date"], dayfirst=False)
    daily_rain.sort_values(by='Date', inplace=True)

    # Final rainfall dataset
    final = pd.merge(path_dd, daily_rain, on='Date')
    final = final.round(decimals=0)
    final = final[final.iloc[:, 3] >= rainfall_threshold]

    rain_pick = final.iloc[:, 2]
    rain_pick = rain_pick.to_numpy()
    rain_pick = np.array([int(v) for v in rain_pick])
    rain_pick2 = -100 * np.ones((1000))
    rain_pick2[0:len(rain_pick)] = rain_pick
    rain = np.append(rain, rain_pick2)
    maxLa = max(maxLa, len(rain_pick))

    rain = rain.reshape([len(rain_pick2), 1], order='F') #rain.reshape([len(rain_pick2), len(years)], order='F')
    rain = np.ceil(rain[0:maxLa] / int(delta_t))
    return rain
