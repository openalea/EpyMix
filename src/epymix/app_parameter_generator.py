import numpy as np

from epymix.rain import rain as rain ## f_rain
from epymix.inoculum import inoculum ## inoculum
from epymix.configuration import configuration
from epymix.SEIR import SEIR ## SEIR fonction principale
from epymix.dispersion_gradient import dispersion_kernel_rust, dispersion_kernel_septo
from epymix.growth_companion import growth_pois

def parameter_set(disease_par, delta_t0, delta_t):
    if disease_par == "septo_par":
        ## MAIN INPUT PARAMETERS
        disease = "septo"
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
        ### INOCULUM PARAMETERS
        inoc_init_abs = 20000000 # inoc_init_abs: initial inoculum intensity
        ng_ext0_abs = int(20000*delta_t/delta_t0) # ng_ext0_abs: external cloud intensity
        ### SPORE DISPERSION
        day_length = (24/(2*delta_t))*60*60
        alpha_asco = 3 # coefficient of dispersal (n m-1;Fitt et al 1987)
        radius_asco = 5
        alpha_pycnid = 0.2 * 0.0001 # coefficient of dispersal (m² s-1; Yang et al 1991)
        radius_pycnid = 5
        alpha_ure = 3
        radius_ure = 5
    
    elif disease_par == "rust_par":
        ## MAIN INPUT PARAMETERS
        disease = "rust"
        ## E-I TRANSITION PARAMETERS
        delta_ei = 5*int(delta_t0/delta_t)
        lambd = 10*int(delta_t0/delta_t) # 100 dd %% latent duration
        ## EPIDEMIC PARAMETERS
        s0 = 0.0001 # 0.0001 %% lesion size (µm²)
        pi_inf0 = 0.0002*delta_t/delta_t0 # 0.0002 %% spore probability infection
        rho = 0.01*delta_t/delta_t0  # 0.01 %% spore mortality in P reservoir
        psi = 0.3  # 0 %% pycnide emptying rate by rain (only for septoriose)
        gamma = 0  # 0 %% virulence parameter
        theta = 0.01  # 0.01 %% spore intercropping survival rate
        sigma = 1500000 # 1500000 %% spore production rate (LAI-1; septo: pycnidiospores by rain))
        sigma_asco = 0.02 * sigma # 0.2*sigma %% (parameter for septoriose only, ascospores by wind)
        inf_begin = 80*int(delta_t0/delta_t)  # 1000 dd %% date of epidemic start (generally between 80 et 130 dd for rust)
        ### INOCULUM PARAMETERS
        inoc_init_abs = 500000 # inoc_init_abs: initial inoculum intensity
        ng_ext0_abs = int(2000*delta_t/delta_t0) # ng_ext0_abs: external cloud intensity
        ### SPORE DISPERSION
        day_length = (24/(2*delta_t))*60*60
        alpha_asco = 3 # 3 coefficient of dispersal (n m-1;Fitt et al 1987)
        radius_asco = 5
        alpha_pycnid = 0.2 * 0.0001 # coefficient of dispersal (m² s-1; Yang et al 1991)
        radius_pycnid =5
        alpha_ure = 3
        radius_ure = 5
    
    return disease, delta_ei, lambd, s0, pi_inf0, rho, psi, gamma, theta, sigma, sigma_asco, inf_begin, inoc_init_abs, ng_ext0_abs, day_length, alpha_asco, radius_asco, alpha_pycnid, radius_pycnid, alpha_ure, radius_ure
