import numpy as np

### FUNCTION
# Define the rotation scenario for several cropping season

### PARAMETERS
# Lr: number of seasons (> 1)
# Lx: number of patch along the x-axis
# Ly: number of patch along the y-axis
# scenario: scenario of rotation (chose: R2ans-asynchrone-damier-50%ble, R2ans-asynchrone-aleatoire-50%ble, etc)

def f_rotation(Lr, Lx, Ly, scenario):

    rotation = np.ones((Lr, Lx, Ly))

    ############
    ############ ROTATION DE 2 ANs
    ############
    if Lr == 2:
        if scenario == "R2ans-asynchrone-damier-50%ble":
        ############## ROTATION DE 2 ANS ASYNCHRONE EN DAMIER avec 50% de ble dans le paysage
            for i in range(0,Lx):
                for j in range(0,Ly):
                    if (i+j)%2 == 0:
                        rotation[1,i,j] = 0
                    else:
                        rotation[0,i,j] = 0
        elif scenario == "R2ans-asynchrone-aleatoire-50%ble":
        ############## ROTATION DE 2 ANS ASYNCHRONE EN MOTIF ALEATOIRE avec 50% de ble dans le paysage
            id = np.random.permutation(Lx * Ly)
            rotation = rotation.reshape([Lr * Lx * Ly])
            rotation[id[0:int(np.floor((1.0/2)*Lx*Ly))]] = 0
            rotation[id[int(np.floor((1.0/2)*Lx*Ly)):len(id)] + (Lx*Ly)]=0
            rotation = rotation.reshape([Lr, Lx, Ly])
        elif scenario == "R2ans-synchrone-50%ble":
        ############## ROTATION DE 2 ANS SYNCHRONE avec 50% de ble dans le paysage
            rotation[1,:,:] = np.zeros((Lx,Ly))

    ############
    ############ ROTATION DE 3 ANS
    ############
    else Lr == 3:
        if scenario == "R3ans-asynchrone-aleatoire-67%ble":
            ############## ROTATION DE 3 ANS ASYNCHRONE EN MOTIF ALEATOIRE avec 67% de ble dans le paysage
            id = np.random.permutation(Lx * Ly)
            rotation = rotation.reshape([Lr * Lx * Ly])
            rotation[id[0:int(np.floor((1.0/3)*Lx*Ly))]] = 0
            rotation[id[int(np.floor((1.0/3) * Lx*Ly)):int(np.floor((2.0/3)*Lx*Ly))] + (Lx*Ly)] = 0
            rotation[id[int(np.floor((2.0/3) * Lx*Ly)):len(id)] + ((Lr-1)*Lx*Ly)]=0
            rotation = rotation.reshape([Lr, Lx, Ly])
        elif scenario == "R3ans-synchrone-67%ble":
        ############## ROTATION DE 3 ANS SYNCHRONE avec 67% de ble dans le paysage
            rotation[Lr-1,:,:] = np.zeros((Lx,Ly))
        elif scenario == "R3ans-asynchrone-aleatoire-33%ble":
        ############## ROTATION DE 3 ANS ASYNCHRONE EN MOTIF ALEATOIRE avec 33% de ble dans le paysage
            id = np.random.permutation(Lx * Ly)
            rotation = rotation.reshape([Lr * Lx * Ly])
            rotation[id[0:int(np.floor((1.0/3)*Lx*Ly))]] = 0
            rotation[id[int(np.floor((1.0/3) * Lx*Ly)):int(np.floor((2.0/3)*Lx*Ly))] + (Lx*Ly)] = 0
            rotation[id[int(np.floor((2.0/3) * Lx*Ly)):len(id)] + ((Lr-1)*Lx*Ly)]=0
            rotation = rotation.reshape([Lr, Lx, Ly])
            rotation = np.logical_not(rotation).astype(int)
        elif scenario == "R3ans-synchrone-33%ble":
        ########### ROTATION DE 3 ANS SYNCHRONE avec 33% de ble dans le paysage
            rotation[1,:,:] = np.zeros((Lx,Ly))
            rotation[2,:,:] = np.zeros((Lx,Ly))
    return rotation
