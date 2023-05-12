import pandas
pandas.set_option('display.max_colwidth', None)
import logging, sys

from weatherdata import WeatherDataHub

ws=WeatherDataHub()
ws.list_resources

meteo=ws.get_ressource(name='Landbruksmeteorologisk tjeneste')
print(meteo.stations)
ds=meteo.data(parameters=[2001],stationId=[5],
            timeStart='2020-06-11', timeEnd='2021-06-11',
            timeZone='Europe/Paris',varname="id",usecache=True, savecache=True,display="ds")
df = ds.to_dataframe()
print(df['2001'])