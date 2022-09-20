import data as data
import os

def test_meteo_path():
    fn = data.meteo_path(1994)
    assert os.path.exists(fn)
