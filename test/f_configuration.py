import os
import numpy as np
import math

### PARAMETRES INITIAUX FONCTION
#Lr = 3 # nombre saison
#scenario = "R3ans-synchrone-33%ble"
#frac_ble = 0.5 ## doit etre inferieur a 1 (fraction de ble dans le champs)

# ### PARAMETRES INITIAUX GLOBAUX
# Lx = 21 # taille de la grille(=paysage) en x
# Ly = 21 # taille de la grille(=paysage) en y
# #rotation = np.ones((Lr,Lx,Ly)) #2 depth, Lx rows, Ly colomns

def f_configuration(Lr, Lx, Ly, scenario_rot, wheat_fraction):
    rotation = np.ones((Lr, Lx, Ly))

    ### MIX OF X% OF WHEAT IN EACH PLOT FOR ALL PLOTS
    if scenario_rot == "uniform":
        rotation = wheat_fraction * rotation

    ### RANDOM PATTERN OF X% OF WHEAT
    elif scenario_rot == "random":
        id = np.random.permutation(Lx * Ly)
        rotation = rotation.reshape([Lr*Lx*Ly])
        rotation[id[0:int(np.floor(Lx*Ly*(1-wheat_fraction)))]] = 0
        rotation = rotation.reshape([Lr, Lx, Ly])

    ### CHESSBOARD PATTTERN WITH 50% OF WHEAT
    elif scenario_rot == "chessboard":
        for i in range(0,Lx):
            for j in range(0,Ly):
                if (i+j)%2 == 0:
                    rotation[0,i,j] = 0

    ### ALTERNATE ROWS
    elif scenario_rot =="alternate":
        for i in range(0,Lx):
            if i % 2 == 1:
                rotation[:,i,:] = 0

    ### ALTERNATE RANKS (ALONG Ly)
    elif scenario_rot =="alternate_rank":
        for i in range(0,Ly):
            if i % 2 == 1:
                rotation[:,:,i] = 0

    ### ALTERNATE STRIPS WITH 2 ROWS PER STRIP
    elif scenario_rot == "alternate_strip2":
        for i in range (0,Lx):
            if i % 4 == 0:
                rotation[:,i:i+2,:] = 0

    ### ALTERNATE STRIPS WITH 3 ROWS PER STRIP
    elif scenario_rot == "alternate_strip3":
        for i in range (0,Lx):
            if i % 6 == 0:
                rotation[:, i:i+3, :] = 0

    ### ALTERNATE PAIRS OF PATCH ALONG Lx
    elif scenario_rot == "alternate_pairs":
        for i in range(0,Lx):
            for j in range(0,Ly):
                if i%2 == 0 and j%4 == 0:
                    rotation[:, i, j:j+2] = 0
                    rotation[:, i+1, j+2:j+3] = 0

    ### ALTERNATE DOUBLE-PAIRS ALONG Lx
    elif scenario_rot == "alternate_doublepairs":
        for i in range(0,Lx):
            if i % 2 == 1:
                rotation[:,i,:] = 0
        for i in range(0,Lx):
            for j in range(0,Ly):
                if i%2 == 0 and j%8 == 0:
                    rotation[:, i, j:j+4] = 0
                    rotation[:, i+1, j:j+4] = 1

    ### TWO SUB-FIELDS
    elif scenario_rot == "two_subs":
        for i in range(0, Lx):
            if i < (Lx/2):
                rotation[:, i, :] = 0

    ### FOUR SUB-FIELDS
    elif scenario_rot == "four_subs":
        for i in range(0, Lx):
            for j in range(0, Ly):
                if i < (Lx/2) and j < (Ly/2):
                    rotation[:, i, j] = 0
                if i >= (Lx/2) and j >= (Ly/2):
                    rotation[:, i, j] = 0

    ### 4-PATCH SQUARE
    elif scenario_rot == "4_square":
        for i in range(0, Lx):
            for j in range(0, Ly):
                if i % 4 == 0 and j % 4 == 0:
                    rotation[:, i:i+2, j:j+2] = 0
                    rotation[:, i+2:i+4, j+2:j+4] = 0

    ### 9-PATCH SQUARES
    elif scenario_rot == "9_square":
        for i in range(0, Lx):
            for j in range(0, Ly):
                if i % 6 == 0 and j % 6 == 0:
                    rotation[:, i:i+3, j:j+3] = 0
                    rotation[:, i+3:i+6, j+3:j+6] = 0

    ############ TEST DIFFERENT PROPORTIONS ACCORDING TO ARRANGEMENT ############
    ### 1/5 IN ALTERNATE ROWS
    elif scenario_rot == "1_5_alternate":
        for i in range(0, Lx):
            if i % 5 == 0:
                rotation[:, i, :] = 0

    ### 2/5 IN ALTERNATE ROWS
    elif scenario_rot == "2_5_alternate":
        for i in range(0, Lx):
            for j in range(0, Lx):
                if i % 5 == 0:
                    rotation[:, i, :] = 0
                if j % 5 == 2:
                    rotation[:, j, :] = 0

    ### 3/5 IN ALTERNATE ROWS
    elif scenario_rot == "3_5_alternate":
        for i in range(0, Lx):
            for j in range(0, Lx):
                if i % 5 == 0:
                    rotation[:, i, :] = 0
                if j % 5 == 2:
                    rotation[:, j:j+2, :] = 0

    ### 4/5 IN ALTERNATE ROWS
    elif scenario_rot == "4_5_alternate":
        for i in range(0, Lx):
            if i % 5 == 1:
                rotation[:, i:i+4, :] = 0

    ### 1/5 IN 4-PATCH SQUARE
    elif scenario_rot == "1_5_square":
        for i in range(0, Lx):
            for j in range(0, Ly):
                if i % 10 == 0 and j % 10 == 0:
                    rotation[:, i:i+2, j:j+2] = 0
                    rotation[:, i+2:i+4, j+4:j+6] = 0
                    rotation[:, i+4:i+6, j+8:j+10] = 0
                    rotation[:, i+6:i+8, j+2:j+4] = 0
                    rotation[:, i+8:i+10, j+6:j+8] = 0

    ### 2/5 IN 4-PATCH SQUARE
    elif scenario_rot == "2_5_square":
        for i in range(0, Lx):
            for j in range(0, Ly):
                if i % 10 == 0 and j % 10 == 0:
                    rotation[:, i:i+2, j:j+2] = 0
                    rotation[:, i:i+2, j+4:j+6] = 0
                    rotation[:, i+2:i+4, j+2:j+4] = 0
                    rotation[:, i+2:i+4, j+6:j+8] = 0
                    rotation[:, i+4:i+6, j+4:j+6] = 0
                    rotation[:, i+4:i+6, j+8:j+10] = 0
                    rotation[:, i+6:i+8, j:j+2] = 0
                    rotation[:, i+6:i+8, j+6:j+8] = 0
                    rotation[:, i+8:i+10, j+2:j+4] = 0
                    rotation[:, i+8:i+10, j+8:j+10] = 0

    ### 3/5 IN 4-PATCH SQUARE
    elif scenario_rot == "3_5_square":
        for i in range(0, Lx):
            for j in range(0, Ly):
                if i % 10 == 0 and j % 10 == 0:
                    rotation[:, i:i+2, j:j+2] = 0
                    rotation[:, i:i+2, j+4:j+8] = 0
                    rotation[:, i+2:i+4, j+2:j+4] = 0
                    rotation[:, i+2:i+4, j+6:j+10] = 0
                    rotation[:, i+4:i+6, j:j+2] = 0
                    rotation[:, i+4:i+6, j+4:j+6] = 0
                    rotation[:, i+4:i+6, j+8:j+10] = 0
                    rotation[:, i+6:i+8, j:j+4] = 0
                    rotation[:, i+6:i+8, j+6:j+8] = 0
                    rotation[:, i+8:i+10, j+2:j+6] = 0
                    rotation[:, i+8:i+10, j+8:j+10] = 0

    ### 4/5 IN 4-PATCH SQUARE
    elif scenario_rot == "4_5_square":
        for i in range(0, Lx):
            for j in range(0, Ly):
                if i % 10 == 0 and j % 10 == 0:
                    rotation[:, i:i+2, j:j+8] = 0
                    rotation[:, i+2:i+4, j+2:j+10] = 0
                    rotation[:, i+4:i+6, j+4:j+10] = 0
                    rotation[:, i+4:i+6, j:j+2] = 0
                    rotation[:, i+6:i+8, j:j+4] = 0
                    rotation[:, i+6:i+8, j+6:j+10] = 0
                    rotation[:, i+8:i+10, j:j+6] = 0
                    rotation[:, i+8:i+10, j+8:j+10] = 0

    return rotation


