from epymix.f_rain import f_rain


def test_f_rain():
    rain = f_rain(1994)
    assert rain.shape == (82, 1)
    rain = f_rain([1994, 1995])
    assert rain.shape == (82, 2)
    assert rain[-1,1] == -10