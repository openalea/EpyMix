import os
import numpy as np
import math


from epyland.f_rain import f_rain ## f_rain
from epyland.inoculum import inoculum ## inoculum
from epyland.f_rotation import f_rotation ## f_rotation
from epyland.SEIR3 import SEIR ## SEIR fonction principale


parameters = dict(

    ### Parametres generaux (renseignes dans WRL/STB)
    mu=0.03,  # 0.03 %% mortalite des tissus S et E
    nu=0.03,  # nu = mu %% mortalite des tissus infectieux I
    beta_ble=0.09,  # 0.09 %% parametre de croissance du ble
    beta_pois=0.09,  # beta_pois = beta_ble %% parametre de croissance du pois
    s0=0.0001,  # 0.0001 %% taille d'une lesion
    saison=250,  # 2500 dj %% longueur d'une saison culturale
    Cr_ble=140,  # 1400 dj %% date de fin de la croissance du ble
    Cr_pois=140,  # Cr_pois = Cr_ble %% date de fin de la croissance du pois
    pi_inf0=0.0002,  # 0.0002 %% probabilite d'infection d'une spore
    LAIpot=6,  # 6 %% capacite de charge (LAI maximal du couvert)
    ng_ext0_abs=20000,  # 20000 %% spores arrivant via un nuage exterieur au paysage
    ber=1,  # 1 # coeff d'interception des spores (il s'agit d'une loi de Beer-Lambert)
    inoc_init_abs=500000,  # 500000 %% spores presentes initialement dans le reservoir P
    # uniquement utilise dans le scenario d'inoculation d'un focus central

    ### Parametres specifiques (renseignes dans WRL/STB)
    maladie="septo",
    alpha=0.5,  # 0.5 %% fraction des spores sortant de la parcelle
    rho=0.01,  # 0.01 %% mortalite des spores du reservoir P
    psi=0.0,  # 0 %% taux de vidage des pycnides (seulement pour la septoriose)
    gamma=0,  # 0 %% parametre de virulence
    lambd=10,  # 100 dj %% latence
    theta=0.01,  # 0.01 %% taux de survie interculturale des spores
    sigma=1500000,  # 1500000 %% taux de production de spores
    sigma_asco=0,  # 0 %% (parametre pertinent pour la septoriose uniquement)
    rda=5,  # 5 %% rayon de dispersion
    inf_begin=100  # 1000 dj %% date de debut de l'epidemie (typiquement comprise entre 80 et 130 pour la rouille)
)

## Scenario 1 : focus cetral
def test_inoculum_scenario_focuscentral():
    """SEIR + PROPORTION DU COUVERT INFECTE OU RESERVOIR DE SPORES"""
    annees = [1994, 1995]
    rain = f_rain(annees)
    t = 1000
    Lx = 3
    Ly = 3
    rotation = np.ones((1, Lx, Ly))
    inoc_init_abs = parameters['inoc_init_abs']

    inoc_init, ng_ext0 = inoculum(scenario="focus central", frac_inf=1, inoc_init_abs=parameters['inoc_init_abs'], ng_ext0_abs=parameters['ng_ext0_abs'], rotation=rotation)
    desired_inoc_init = np.array([[0, 0, 0],[0, inoc_init_abs, 0],[0, 0, 0]])
    np.testing.assert_allclose(desired_inoc_init, inoc_init)
    assert ng_ext0 == 0
    #TODO make assertion fail for known diff with matlab


## Scenario 2 : inoculum initial
def test_inoculum_scenario_inoculuminitial():
    """SEIR + PROPORTION DU COUVERT INFECTE OU RESERVOIR DE SPORES"""
    annees = [1994, 1995]
    rain = f_rain(annees)
    t = 1000
    Lx = 3
    Ly = 3
    rotation = np.ones((1, Lx, Ly))

    inoc_init, ng_ext0 = inoculum(scenario="inoculum initial", frac_inf=1, inoc_init_abs=parameters['inoc_init_abs'], ng_ext0_abs=parameters['ng_ext0_abs'], rotation=rotation)
    desired_inoc_init =np.ones((Lx, Ly)) * 20000000
    np.testing.assert_allclose(desired_inoc_init, inoc_init)
    assert ng_ext0 == 0
    #TODO make assertion fail for known diff with matlab

def test_inoculum_nuageannuel():
    """SEIR + PROPORTION DU COUVERT INFECTE OU RESERVOIR DE SPORES"""
    annees = [1994, 1995]
    rain = f_rain(annees)
    t = 1000
    Lx = 1
    Ly = Lx
    rotation = np.ones((1, Lx, Ly))

    inoc_init, ng_ext0 = inoculum(scenario="nuage annuel", frac_inf=1, inoc_init_abs=parameters['inoc_init_abs'], ng_ext0_abs=parameters['ng_ext0_abs'], rotation=rotation)
    assert inoc_init == np.array([[0.]])
    assert ng_ext0[0,0,0] == 20000
    #TODO make assertion fail for known diff with matlab
    Nsp, Pth, Poi, Sth, Sus, Lat, Ifc, Ifv, Rem, LAI, Poo, Eps, AUDPC, Scont = SEIR(ng_ext0=ng_ext0,
                                                                                    rain=rain, inoc_init=inoc_init,
                                                                                    rotation=rotation, t=t,
                                                                                    **parameters)