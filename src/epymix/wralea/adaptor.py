import random

from openalea.core import *

from epymix.rain_WD import rain as _rain ## f_rain
from epymix.inoculum import inoculum ## inoculum
from epymix.configuration import configuration
from epymix.SEIR import SEIR ## SEIR fonction principale
from epymix.dispersion_gradient import dispersion_kernel_rust, dispersion_kernel_septo
from epymix.growth_companion import growth_pois as growth_pea


def rain(
        site='Landbruksmeteorologisk tjeneste', 
        time_start='2019-09-01', 
        time_end='2020-09-01', 
        delta_t=10, 
        sowing_date='2019-09-01', 
        rainfall_threshold=3):
    """ Rain or Precipitation from WeatherData"""
    return _rain(site, time_start, time_end, delta_t, sowing_date, rainfall_threshold)


