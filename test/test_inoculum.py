import numpy as np

#from epymix.f_rain import f_rain ## f_rain
from inoculum import inoculum


## Scenario 1 : focus cetral
def test_inoculum_scenario_focuscentral():
    Lx = 3
    Ly = 3
    ng_ext0_abs = 20000
    inoc_init_abs = 500000
    inoc_init, ng_ext0 = inoculum(scenario_ino="focus_central", Lx=Lx, Ly=Ly, frac_inf=1,
                                  inoc_init_abs=inoc_init_abs, ng_ext0_abs=ng_ext0_abs)
    desired_inoc_init = np.array([[0, 0, 0],[0, inoc_init_abs, 0],[0, 0, 0]])
    np.testing.assert_allclose(desired_inoc_init, inoc_init)
    assert ng_ext0 == 0

## Scenario 2 : inoculum initial
def test_inoculum_scenario_inoculuminitial():
    Lx = 3
    Ly = 3
    ng_ext0_abs = 20000
    inoc_init_abs = 500000
    inoc_init, ng_ext0 = inoculum(scenario_ino="inoculum_initial", Lx=Lx, Ly=Ly, frac_inf=1,
                                  inoc_init_abs=inoc_init_abs, ng_ext0_abs=ng_ext0_abs)
    desired_inoc_init =np.ones((Lx, Ly)) * 20000000
    np.testing.assert_allclose(desired_inoc_init, inoc_init)
    assert ng_ext0 == 0
