import os

### FUNCTION
# Manage rainfall data import for septoria, called by the function f_rain

data_dir = os.path.join(os.path.dirname(__file__), 'data')

def meteo_path(year, is_year_start=True):
    """return path of meteo data file"""
    year_start = year
    year_end = year + 1
    if not is_year_start:
        year_start = year -1
        year_end = year
    fn = "rain-events_" + str(year_start) + "-" + str(year_end) + ".txt"
    return os.path.join(data_dir, fn)