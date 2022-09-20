import numpy as np

from epymix.f_rotation import f_rotation


def test_rotation_scenario1():
    sc = "R1an-aleatoire"
    ## Taille de la parcelle
    Lr = 1
    Lx = 3
    Ly = 3
    resistant_fraction = 0.5
    rotation = f_rotation(Lr=Lr, Lx=Lx,Ly=Ly, scenario=sc, resistant_fraction=resistant_fraction)
    assert rotation.shape == (Lr, Lx, Ly)


def test_rotation_scenario2():
    sc = "R1an-damier-50%ble"
    ## Taille de la parcelle
    Lr = 1
    Lx = 3
    Ly = 3
    resistant_fraction=0.5
    rotation = f_rotation(Lr=Lr, Lx=Lx,Ly=Ly, scenario=sc, resistant_fraction=resistant_fraction)
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
    resistant_fraction=0.5
    rotation = f_rotation(Lr=Lr, Lx=Lx,Ly=Ly, scenario=sc, resistant_fraction=resistant_fraction, melange=melange)
    assert rotation.shape == (Lr, Lx, Ly)
    assert rotation[0,0,0] == melange


def test_rotation_scenario4():
    sc = "R2ans-asynchrone-damier-50%ble"
    ## Taille de la parcelle
    Lr = 2
    Lx = 3
    Ly = 3
    resistant_fraction=0.5
    rotation = f_rotation(Lr=Lr, Lx=Lx,Ly=Ly, scenario=sc, resistant_fraction=resistant_fraction)
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
    resistant_fraction=0.5
    rotation = f_rotation(Lr=Lr, Lx=Lx,Ly=Ly, scenario=sc, resistant_fraction=resistant_fraction)
    assert rotation.shape == (Lr, Lx, Ly)
    assert np.count_nonzero(rotation[0,:,:] == 1) == 5


def test_rotation_scenario6():
    sc = "R2ans-synchrone-50%ble"
    ## Taille de la parcelle
    Lr = 2
    Lx = 3
    Ly = 3
    resistant_fraction=0.5
    rotation = f_rotation(Lr=Lr, Lx=Lx,Ly=Ly, scenario=sc, resistant_fraction=resistant_fraction)
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
    resistant_fraction=0.33
    rotation = f_rotation(Lr=Lr, Lx=Lx,Ly=Ly, scenario=sc, resistant_fraction=resistant_fraction)
    assert rotation.shape == (Lr, Lx, Ly)
    assert np.count_nonzero(rotation[0,:,:] == 1) == 6


def test_rotation_scenario8():
    sc = "R3ans-synchrone-67%ble"
    ## Taille de la parcelle
    Lr =3
    Lx = 3
    Ly = 3
    resistant_fraction=0.33
    rotation = f_rotation(Lr=Lr, Lx=Lx,Ly=Ly, scenario=sc, resistant_fraction=resistant_fraction)
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
    resistant_fraction=0.67
    rotation = f_rotation(Lr=Lr, Lx=Lx,Ly=Ly, scenario=sc, resistant_fraction=resistant_fraction)
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
    resistant_fraction=0.67
    rotation = f_rotation(Lr=Lr, Lx=Lx,Ly=Ly, scenario=sc, resistant_fraction=resistant_fraction)
    assert rotation.shape == (Lr, Lx, Ly)
    desired_rotation1 = np.ones((Lx, Ly))
    np.testing.assert_allclose(rotation[0, :, :], desired_rotation1)
    desired_rotation2 = np.zeros((Lx, Ly))
    np.testing.assert_allclose(rotation[1, :, :], desired_rotation2)
    desired_rotation3 = np.zeros((Lx, Ly))
    np.testing.assert_allclose(rotation[2, :, :], desired_rotation3)