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


def test_rotation_scenario1():
    sc = "R1an-aleatoire"
    ## Taille de la parcelle
    Lr = 1
    Lx = 3
    Ly = 3
    frac_ble = 0.5
    rotation = f_rotation(Lr=Lr, Lx=Lx,Ly=Ly, scenario=sc, frac_ble=frac_ble)
    assert rotation.shape == (Lr, Lx, Ly)


def test_rotation_scenario2():
    sc = "R1an-damier-50%ble"
    ## Taille de la parcelle
    Lr = 1
    Lx = 3
    Ly = 3
    rotation = f_rotation(Lr=Lr, Lx=Lx,Ly=Ly, scenario=sc)
    assert rotation.shape == (Lr, Lx, Ly)
    desired_rotation = np.array([[[0,1,0], [1,0,1],[0,1,0]]])
    np.testing.assert_allclose(rotation, desired_rotation)


def test_rotation_scenario3():
    sc = "R1an-melange-uniforme"
    ## Taille de la parcelle
    Lr = 1
    Lx = 3
    Ly = 3
    melange = 0.5
    rotation = f_rotation(Lr=Lr, Lx=Lx,Ly=Ly, scenario=sc, melange=melange)
    assert rotation.shape == (Lr, Lx, Ly)
    assert rotation[0,0,0] == melange


def test_rotation_scenario4():
    sc = "R2ans-asynchrone-damier-50%ble"
    ## Taille de la parcelle
    Lr = 2
    Lx = 3
    Ly = 3
    rotation = f_rotation(Lr=Lr, Lx=Lx,Ly=Ly, scenario=sc)
    assert rotation.shape == (Lr, Lx, Ly)
    desired_rotation1 = np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]])
    np.testing.assert_allclose(rotation[0,:,:], desired_rotation1)
    desired_rotation2 = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    np.testing.assert_allclose(rotation[1,:,:], desired_rotation2)


def test_rotation_scenario5():
    sc = "R2ans-asynchrone-aleatoire-50%ble"
    ## Taille de la parcelle
    Lr = 2
    Lx = 3
    Ly = 3
    rotation = f_rotation(Lr=Lr, Lx=Lx,Ly=Ly, scenario=sc)
    assert rotation.shape == (Lr, Lx, Ly)
    assert np.count_nonzero(rotation[0,:,:] == 1) == 5


def test_rotation_scenario6():
    sc = "R2ans-synchrone-50%ble"
    ## Taille de la parcelle
    Lr = 2
    Lx = 3
    Ly = 3
    rotation = f_rotation(Lr=Lr, Lx=Lx,Ly=Ly, scenario=sc)
    assert rotation.shape == (Lr, Lx, Ly)
    desired_rotation1 = np.ones((Lx, Ly))
    np.testing.assert_allclose(rotation[0,:,:], desired_rotation1)
    desired_rotation2 = np.zeros((Lx, Ly))
    np.testing.assert_allclose(rotation[1,:,:], desired_rotation2)


def test_rotation_scenario7():
    sc = "R3ans-asynchrone-aleatoire-67%ble"
    ## Taille de la parcelle
    Lr =3
    Lx = 3
    Ly = 3
    rotation = f_rotation(Lr=Lr, Lx=Lx,Ly=Ly, scenario=sc)
    assert rotation.shape == (Lr, Lx, Ly)
    assert np.count_nonzero(rotation[0,:,:] == 1) == 6


def test_rotation_scenario8():
    sc = "R3ans-synchrone-67%ble"
    ## Taille de la parcelle
    Lr =3
    Lx = 3
    Ly = 3
    rotation = f_rotation(Lr=Lr, Lx=Lx,Ly=Ly, scenario=sc)
    assert rotation.shape == (Lr, Lx, Ly)
    desired_rotation1 = np.ones((Lx, Ly))
    np.testing.assert_allclose(rotation[0, :, :], desired_rotation1)
    desired_rotation2 = np.zeros((Lx, Ly))
    np.testing.assert_allclose(rotation[2, :, :], desired_rotation2)


def test_rotation_scenario9():
    sc = "R3ans-asynchrone-aleatoire-33%ble"
    ## Taille de la parcelle
    Lr =3
    Lx = 3
    Ly = 3
    rotation = f_rotation(Lr=Lr, Lx=Lx,Ly=Ly, scenario=sc)
    assert rotation.shape == (Lr, Lx, Ly)
    assert np.count_nonzero(rotation[0,:,:] == 1) == 3
    assert np.count_nonzero(rotation[1, :, :] == 1) == 3
    assert np.count_nonzero(rotation[2, :, :] == 1) == 3

def test_rotation_scenario9():
    sc = "R3ans-synchrone-33%ble"
    ## Taille de la parcelle
    Lr =3
    Lx = 3
    Ly = 3
    rotation = f_rotation(Lr=Lr, Lx=Lx, Ly=Ly, scenario=sc)
    assert rotation.shape == (Lr, Lx, Ly)
    desired_rotation1 = np.ones((Lx, Ly))
    np.testing.assert_allclose(rotation[0, :, :], desired_rotation1)
    desired_rotation2 = np.zeros((Lx, Ly))
    np.testing.assert_allclose(rotation[1, :, :], desired_rotation2)
    desired_rotation3 = np.zeros((Lx, Ly))
    np.testing.assert_allclose(rotation[2, :, :], desired_rotation3)