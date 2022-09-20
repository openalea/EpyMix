import numpy as np

### FUNCTION
# Growth function for the companion crop only

### PARAMETERS
# t: length of the experiment
# season: length of a cropping season
# arrangement: patch spatial arrangement (from f_configuration function)
# mu_companion: mortality rate of the companion species (LAI/10dd)
# beta_companion: growth parameter of the companion crop (LAI/10dd)
# end_companion: date of growth end for the companion crop
# LAI_K: carrying capacity (Maximum canopy LAI)

def growth_pois(t, season, arrangement, mu_companion, beta_companion, end_companion, LAI_K):
    ### Rotation parameters; for the rotation function
    Lr = arrangement.shape[0] # rotation period
    Lx = arrangement.shape[1] # number of fileds along the x axis
    Ly = arrangement.shape[2] # number of fileds along the y axis

    ### Canopy component
    Pth_inde = np.zeros((t,Lx,Ly))   # Ph = Companion : dead + aline (total companion)
    Poi_inde = np.zeros((t,Lx,Ly))   # Poi = companion alive

    ### Initialisation of LAI_K_component
    LAI_K_component = 0.0

    ### MAIN FUNCTION
    for i in range(0, t):
        if np.mod(i, season) == 0:
            res_frac = arrangement[int((np.floor(i / season) % Lr)), :, :]
            LAI_K_component = (1 - res_frac) * LAI_K

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
