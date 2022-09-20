from f_rain import f_rain

def test_f_rain():
    years=1994
    delta_t = 10
    rain = f_rain(years=years, delta_t=delta_t)
    assert rain.shape == (82, 1)
    rain = f_rain([1994, 1995], delta_t=delta_t)
    assert rain.shape == (82, 2)
    assert rain[-1,1] == -10