import numpy as np

### FUNCTION
# Parameterize the initial spore inoculum (spatial position(s) within the grid/field and intensity) (inoc_init)
# and the intensity of spore external cloud (ng_ext0)

### PARAMETERS
# scenario_ino: which scenario of initial inoculum (chose: central_focus, initial_inoculum, annual_cloud)
# Lx: number of patch along the x-axis
# Ly: number of patch along the y-axis
# frac_inf: fraction of patches within the field inoculated
# inoc_init_abs: initial inoculum intensity
# ng_ext0_abs: external cloud intensity

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