import os
import numpy as np
import math
import matplotlib.pyplot as plt

from .f_rain import f_rain ## f_rain
from .inoculum import inoculum ## inoculum
from .f_rotation import f_rotation ## f_rotation
from .f_configuration import f_configuration
from .SEIR_ERIN import SEIR ## SEIR fonction principale
from .f_dispersion_gradient import dispersion_kernel_rust, dispersion_kernel_septo
from .f_growth_companion import growth_pois

### BE CAREFUL
### CHECK Lx, Ly, RDA, DELTA, BER, SCENARIO

## MAIN INPUT PARAMETERS
disease = "septo"
delta_t0 = 10 # constant, the model has been parameterise such as t = 10 degree-day
delta_t = 10 # time step
n_season = 1 # number of season
t = n_season*250*int(delta_t0/delta_t)
season = 250*int(delta_t0/delta_t)  # 2500 dd %% length of a cropping season
delta_companion = 0 # growth start lag of the companion crop (dd), negative: companion before, positive: companion after but for i<delta Poi=0

### ROTATION SCENARIO (Lx,Ly,Lr)
### f_rotation(Lr, Lx, Ly, scenario, frac_ble=1, melange=1)
### f_configuration(Lr, Lx, Ly, scenario, resistant_fraction)
### return rotation
#rotation = np.ones((1, 1, 1))*resistant_fraction # wheat fraction
Lr=1; Lx=1; Ly=1; scenario_rot='uniform'; wheat_fraction=0.5
rotation = f_configuration(Lr, Lx, Ly, scenario_rot, wheat_fraction)

## GROWTH PARAMETERS
mu_wheat = 0.03 * delta_t / delta_t0  # 0.03 %% mortality rate of S and E tissues (LAI/10dd)
nu = 0.03 * delta_t / delta_t0  # nu = mu %% mortality of I infectious tissues (LAI/10dd)
mu_companion = 0.03 * delta_t / delta_t0  # 0.03 %% mortality rate of the companion species (LAI/10dd)
beta_wheat = 0.09 * delta_t / delta_t0  # 0.09 %% wheat growth parameter (LAI/10dd)
beta_companion = 0.09 * delta_t / delta_t0  # beta_companion = beta_wheat %% growth parameter of the companion crop (LAI/10dd)
end_wheat = 140 * int(delta_t0 / delta_t)  # 1400 dj %% date of wheat growth end
end_companion = 140 * int(delta_t0 / delta_t)  # end_companion = end_wheat %% date of growth end for the companion crop
LAI_K = 6  # 6 %% carrying capacity (Maximum canopy LAI)
ber_wheat = 1  # 1 # wheat spore interception coefficient (the Beer-Lambert law)
ber_companion = 1  # 1 # spore interception coefficient of the companion species (the Beer-Lambert law)
h_wheat = 1  # wheat height
h_companion = 1  # companion height
Pth_inde, Poi_inde = growth_pois(t=t, season=season, rotation=rotation,
                       mu_companion=mu_companion, beta_companion=beta_companion, end_companion=end_companion, LAI_K=LAI_K)

## E-I TRANSITION PARAMETERS
delta_ei = 5*int(delta_t0/delta_t)
lambd = 20*int(delta_t0/delta_t) # 200 dd %% latent duration

## EPIDEMIC PARAMETERS
s0 = 0.0001 # 0.0001 %% lesion size (µm²)
pi_inf0 = 0.0002 # 0.0002 %% spore probability infection
rho = 0.002*delta_t/delta_t0  # 0.01 %% spore mortality in P reservoir
psi = 0.3  # 0.3 %% pycnide emptying rate by rain (only for septoriose)
gamma = 0  # 0 %% virulence parameter
theta = 0.15  # 0.015 %% spore intercropping survival rate
sigma = 45000000  # 50000000 %% spore production rate (septo: pycnidiospores by rain)
sigma_asco = 0.2 * sigma # 0.2*sigma %% (parameter for septoriose only, ascospores by wind)
inf_begin = 0*int(delta_t0/delta_t)  #  1000 dd %% date of epidemic start (generally between 80 et 130 dd for rust)

### RAIN PARAMETER
### f_rain, return rain
annees = np.arange(2000,2000+n_season,1) #1995: défavorable; 1997: moyenne, 2000: très favorable
annees = annees.tolist()
rain = f_rain(annees, delta_t)

### INOCULUM PARAMETERS
### inoculum(scenario, frac_inf, inoc_init_abs, ng_ext0_abs, rotation)
### return inoc_init, ng_ext0
# inoc_init_abs = 20000000  # 20000000 %% spores initially present in reservoir P
# ng_ext0_abs = int(20000*delta_t/delta_t0) # 20000 %% spores coming from a cloud external to the landscape
#
# inoc_init = inoc_init_abs  # for the init_saison function in SEIR
# ng_ext0 = ng_ext0_abs
scenario_ino = 'initial_inoculum'; frac_inf = 1; inoc_init_abs = 20000000; ng_ext0_abs = int(20000*delta_t/delta_t0)
inoc_init, ng_ext0 = inoculum(scenario_ino, Lx, Ly, frac_inf, inoc_init_abs, ng_ext0_abs)


### SPORE DISPERSION
### dispersion_kernel(disease, rda, alpha)
### return Disp, C_Disp
day_length = (24/(2*delta_t))*60*60
alpha_asco = 3 # coefficient of dispersal (n m-1;Fitt et al 1987)
radius_asco = 5
alpha_pycnid = 0.2 * 0.0001 # coefficient of dispersal (m² s-1; Yang et al 1991)
radius_pycnid = 5
alpha_ure = 3
radius_ure = 5

kernel_asco, C_Disp_asco, kernel_pycnid, C_Disp_pycnid = dispersion_kernel_septo(day_length, alpha_asco, radius_asco, alpha_pycnid, radius_pycnid)
kernel_ure, C_Disp_ure = dispersion_kernel_rust(day_length, alpha_ure, radius_ure)


### SEIR FUNCTION
Nsp, Pth, Poi, Sth, Sus, Lat, Ifc, Ifv, Rem, LAI, LAI_wheat, Poo, Eps, AUDPC, Scont = \
    SEIR(t=t , delta_t0=delta_t0, delta_t=delta_t, season=season, delta_companion=delta_companion,
    disease=disease, rain=rain, rotation=rotation, inoc_init=inoc_init, ng_ext0=ng_ext0,
    mu_wheat=mu_wheat, nu=nu, beta_wheat=beta_wheat, #beta_companion=beta_companion, end_companion=end_companion
    end_wheat=end_wheat, LAI_K=LAI_K, ber_wheat=ber_wheat, ber_companion=ber_companion, Pth_inde=Pth_inde, Poi_inde=Poi_inde,
    h_wheat=h_wheat, h_companion=h_companion,
    lambd=lambd, delta_ei=delta_ei,
    s0=s0,pi_inf0=pi_inf0, rho=rho, psi=psi, gamma=gamma, theta=theta, sigma=sigma, sigma_asco=sigma_asco, inf_begin=inf_begin,
    C_Disp_ure=C_Disp_ure, kernel_ure=kernel_ure, C_Disp_asco=C_Disp_asco, kernel_asco=kernel_asco,
    C_Disp_pycnid=C_Disp_pycnid, kernel_pycnid=kernel_pycnid)

# ## CSV file
T = [*range(0,t)]
Sth = np.mean(Sth, axis=(1,2))
Pth = np.mean(Pth, axis=(1,2))
Poi = np.mean(Poi, axis=(1,2))
Lat = np.mean(Lat, axis=(1,2))
Ifc = np.mean(Ifc, axis=(1,2))
Ifv = np.mean(Ifv, axis=(1,2))
Sus = np.mean(Sus, axis=(1,2))
Rem = np.mean(Rem, axis=(1,2))
Nsp = np.mean(Nsp, axis=(1,2))
LAI = np.mean(LAI, axis=(1,2))
LAI_wheat = np.mean(LAI_wheat, axis=(1,2))
Poo = np.mean(Poo, axis=(1,2))
AUDPC = np.mean(AUDPC, axis=(1,2))
Eps = np.mean(Eps, axis=(1,2))
Scont = np.mean(Scont, axis=(1,2))

# temp = np.column_stack((T, Sth, Pth, Poi, Lat, Ifc, Ifv, Sus, Rem, Nsp, LAI, LAI_wheat, Poo, AUDPC, Eps, Scont))
# np.savetxt("septo_experiment_05.csv", temp,
#            header= ("t; Sth; Pth; Poi; Lat; Ifc; Ifv; Sus; Rem; Nsp; LAI; LAI_wheat; Poo; AUDPC; Eps; Scont"), comments='',
#            delimiter=';')

plt.plot(T, Sth, color='black')
plt.plot(T, Sus, color='green')
plt.plot(T, Poi, color='brown')
plt.plot(T, Ifv, color='red')
plt.plot(T, Ifc, color='red',linestyle="--")