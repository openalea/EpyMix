import os
import numpy as np
import math

### PARAMETRES INITIAUX FONCTION
#Lr = 3 # nombre saison
#scenario = "R3ans-synchrone-33%ble"
#frac_ble = 0.5 ## doit etre inferieur a 1 (fraction de ble infectee au debut?)
#melange = 0.2

# ### PARAMETRES INITIAUX GLOBAUX
# Lx = 21 # taille de la grille(=paysage) en x
# Ly = 21 # taille de la grille(=paysage) en y
# #rotation = np.ones((Lr,Lx,Ly)) #2 depth, Lx rows, Ly colomns
# #print(rotation)

#### ECRITURE FONCTION



def f_rotation(Lr, Lx, Ly, scenario, resistant_fraction, melange=1):

    rotation = np.ones((Lr, Lx, Ly))
    ############
    ############ PAS DE ROTATION
    ############
    if Lr == 1:
        if scenario == "R1an-aleatoire":
        ############MOTIF ALEATOIRE
            motif = "motif aleatoire"
            #pct_ble = 100 * frac_ble
            id = np.random.permutation(Lx * Ly)
            rotation = rotation.reshape([Lr*Lx*Ly])
            rotation[id[0:int(np.floor(Lx*Ly*(1-resistant_fraction)))]] = 0
            rotation = rotation.reshape([Lr, Lx, Ly])
            rotation != 0

        elif scenario == "R1an-damier-50%ble":
        ############MOTIF EN DAMIER avec 50% de ble
            motif = "damier"
            pct_ble = 50
            for i in range(0,Lx):
                for j in range(0,Ly):
                    if (i+j)%2 == 0:
                        rotation[0,i,j] = 0
        elif scenario == "R1an-melange-uniforme":
        ##############Melange avec X% de LAI ble
            motif = ("melange de " + str(melange*100) + " % de ble uniforme")
            rotation = melange * rotation

    ############
    ############ ROTATION DE 2 ANs
    ############
    elif Lr == 2:
        if scenario == "R2ans-asynchrone-damier-50%ble":
        ############## ROTATION DE 2 ANS ASYNCHRONE EN DAMIER avec 50% de ble dans le paysage
            motif = "rotation asynchrone en damier"
            part_ble = 50
            for i in range(0,Lx):
                for j in range(0,Ly):
                    if (i+j)%2 == 0:
                        rotation[1,i,j] = 0
                    else:
                        rotation[0,i,j] = 0
        elif scenario == "R2ans-asynchrone-aleatoire-50%ble":
        ############## ROTATION DE 2 ANS ASYNCHRONE EN MOTIF ALEATOIRE avec 50% de ble dans le paysage
            motif = "rotation asynchrone aleatoire"
            part_ble = 50
            id = np.random.permutation(Lx * Ly)
            rotation = rotation.reshape([Lr * Lx * Ly])
            rotation[id[0:int(np.floor((1.0/2)*Lx*Ly))]] = 0
            rotation[id[int(np.floor((1.0/2)*Lx*Ly)):len(id)] + (Lx*Ly)]=0
            rotation = rotation.reshape([Lr, Lx, Ly])
        elif scenario == "R2ans-synchrone-50%ble":
        ############## ROTATION DE 2 ANS SYNCHRONE avec 50% de ble dans le paysage
            motif = "rotation synchrone"
            part_ble = 50
            rotation[1,:,:] = np.zeros((Lx,Ly))

    ############
    ############ ROTATION DE 3 ANS
    ############
    elif Lr == 3:
        if scenario == "R3ans-asynchrone-aleatoire-67%ble":
            ############## ROTATION DE 3 ANS ASYNCHRONE EN MOTIF ALEATOIRE avec 67% de ble dans le paysage
            motif = "rotation asynchrone aleatoire"
            part_ble = 67
            id = np.random.permutation(Lx * Ly)
            rotation = rotation.reshape([Lr * Lx * Ly])
            rotation[id[0:int(np.floor((1.0/3)*Lx*Ly))]] = 0
            rotation[id[int(np.floor((1.0/3) * Lx*Ly)):int(np.floor((2.0/3)*Lx*Ly))] + (Lx*Ly)] = 0
            rotation[id[int(np.floor((2.0/3) * Lx*Ly)):len(id)] + ((Lr-1)*Lx*Ly)]=0
            rotation = rotation.reshape([Lr, Lx, Ly])
        elif scenario == "R3ans-synchrone-67%ble":
        ############## ROTATION DE 3 ANS SYNCHRONE avec 67% de ble dans le paysage
            motif = "rotation synchrone"
            part_ble = 67
            rotation[Lr-1,:,:] = np.zeros((Lx,Ly))
        elif scenario == "R3ans-asynchrone-aleatoire-33%ble":
        ############## ROTATION DE 3 ANS ASYNCHRONE EN MOTIF ALEATOIRE avec 33% de ble dans le paysage
            motif = "rotation asynchrone aleatoire"
            part_ble = 33
            id = np.random.permutation(Lx * Ly)
            rotation = rotation.reshape([Lr * Lx * Ly])
            rotation[id[0:int(np.floor((1.0/3)*Lx*Ly))]] = 0
            rotation[id[int(np.floor((1.0/3) * Lx*Ly)):int(np.floor((2.0/3)*Lx*Ly))] + (Lx*Ly)] = 0
            rotation[id[int(np.floor((2.0/3) * Lx*Ly)):len(id)] + ((Lr-1)*Lx*Ly)]=0
            rotation = rotation.reshape([Lr, Lx, Ly])
            rotation = np.logical_not(rotation).astype(int)
        elif scenario == "R3ans-synchrone-33%ble":
        ########### ROTATION DE 3 ANS SYNCHRONE avec 33% de ble dans le paysage
            motif = "rotation synchrone"
            part_ble = 33
            rotation[1,:,:] = np.zeros((Lx,Ly))
            rotation[2,:,:] = np.zeros((Lx,Ly))
    return rotation

#f_rotation(3, 'R3ans-asynchrone-aleatoire-33%ble', 0.5, 0.5)