import os
import numpy as np
import math

# #### PARAMETRES FONCTION
# #scenario = "inoculum initial"
# #frac_inf = 0.1 ## doit etre inferieur a 1 (fraction infectee au debut?)
#
# #### PARAMETRES INITIAUX GLOBAUX
# inoc_init_abs = 500000 # spores presents initialement dans le reservoir
# ng_ext0_abs = 20000
# Lx = 21 # taille de la grille(=paysage) en x
# Ly = 21 # taille de la grille(=paysage) en y
# rotation = np.zeros((1,Lx,Ly)) #2 depth, Lx rows, Ly colomns

def inoculum(scenario_ino, Lx, Ly, frac_inf, inoc_init_abs, ng_ext0_abs):
    inoc_init = np.zeros((Lx, Ly))

    ### INOCULUM FROM A UNIQUE FOCUS
    if scenario_ino == "central_focus":
        #rotation[0, int(np.ceil(Lx/2))-1, int(np.ceil(Ly/2))-1] = 1
        inoc_init[int(np.ceil(Lx/2))-1, int(np.ceil(Ly/2))-1] = inoc_init_abs
        ng_ext0 = 0

    ### INOCULATION OF X% OF PLOTS AT THE BEGINNING OF THE SIM
    elif scenario_ino == "initial_inoculum":
        ng_ext0 = ng_ext0_abs
        for i in range(0, Lx):
            for j in range(0, Ly):
                if np.random.uniform(0, 1) < frac_inf:
                    inoc_init[i, j] = inoc_init_abs

    #### INOCULATION OF X% OF PLOTS AT EACH SEASON BY AN EXTERNAL SPORE CLOUD
    elif scenario_ino == "annual_cloud":
        M_nuage_pre = np.zeros((20 * Lx * Ly))
        for i in range(0, 20):
            id = np.random.permutation(Lx * Ly)
            M_nuage_pre[id[0:int(np.floor(frac_inf * Lx * Ly))] + (i * Lx * Ly)] = 1
            M_nuage = M_nuage_pre.reshape([20, Lx, Ly])
        ng_ext0 = ng_ext0_abs * M_nuage
    else:
        print('Error in the scenario', scenario_ino)
    return inoc_init, ng_ext0