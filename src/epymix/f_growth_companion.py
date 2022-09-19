import os
import numpy as np
import math

def growth_pois(t, season, rotation, mu_companion, beta_companion, end_companion, LAI_K):
    ### Rotation parameters; for the rotation function
    Lr = rotation.shape[0] # rotation period
    Lx = rotation.shape[1] # number of fileds along the x axis
    Ly = rotation.shape[2] # number of fileds along the y axis

    ### Canopy component
    Pth_inde = np.zeros((t,Lx,Ly))   # Ph = Companion : dead + aline (total companion)
    Poi_inde = np.zeros((t,Lx,Ly))   # Poi = companion alive

    ### Initialisation of LAI_K_component
    LAI_K_component = 0.0

    ### MAIN FUNCTION
    for i in range(0, t):
        if np.mod(i, season) == 0:
            ### ble = matrix (Lx, Ly), represents the wheat proportion in landscape fields
            ### ex: [0 0 0 ; 1 1 1 ; 0.5 0.5 0.5] represents one landscape
            ### 1st raw of fields: cropped without wheat; 2nd: wheat only; 3rd: mix with 50% of wheat
            res_frac = rotation[int((np.floor(i / season) % Lr)), :, :]  # rotation(:,:, annee de la rotation)
            LAI_K_component = (1 - res_frac) * LAI_K  # Si on suppose que le pois fait autant de LAI que le ble

            ###Canopy initialisation
            pth0 = LAI_K_component / 1000.0
            Pth_inde[i, :, :] = pth0 * np.ones((Lx, Ly))
            Poi_inde[i, :, :] = pth0 * np.ones((Lx, Ly))

        else:
            pth_inde = Pth_inde[i-1, :, :]
            poi_inde = Poi_inde[i-1, :, :]
            ### Companion crop growth
            crP = beta_companion * (pth_inde) * (1 - pth_inde / (LAI_K_component + (LAI_K_component == 0))) *\
                  (np.mod(i, season) < end_companion)

            ### Updating canopy descriptive variables
            Pth_inde[i,:,:] = pth_inde + crP
            Poi_inde[i,:,:] = poi_inde + crP - mu_companion * poi_inde * (np.mod(i,season) >= end_companion)
    return Pth_inde, Poi_inde
