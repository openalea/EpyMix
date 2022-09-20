import numpy as np
from scipy import ndimage

### FUNCTION
# Main function with crop growth and SEIR functions

### PARAMETERS
# See output files

def SEIR(t, delta_t0, delta_t, season, delta_companion,
         disease, rain, inoc_init, ng_ext0, arrangement,
         mu_wheat, nu, beta_wheat, end_wheat, LAI_K, ber_wheat, ber_companion, Pth_inde, Poi_inde, # beta_companion, end_companion
         h_wheat, h_companion,
         lambd, delta_ei,
         s0, pi_inf0, rho, psi, gamma, theta, sigma, sigma_asco, inf_begin,
         C_Disp_asco, kernel_asco, C_Disp_pycnid, kernel_pycnid, C_Disp_ure, kernel_ure):

    ### arrangement parameters; for the 'arrangement' function
    Lr = arrangement.shape[0] # number of seasons
    Lx = arrangement.shape[1] # number of fileds along the x axis
    Ly = arrangement.shape[2] # number of fileds along the y axis

    ### MAIN STATE VARIABLES
    Pth = np.zeros((t,Lx,Ly))   # companion crop, alive and dead (total companion crop)
    Poi = np.zeros((t,Lx,Ly))   # living companion crop
    Sth = np.zeros((t,Lx,Ly))   # theoretical total surface S (without disease)
    Sus = np.zeros((t,Lx,Ly))   # healthy surface S (non-infected)
    Lat = np.zeros((t,Lx,Ly))   # latent surface E (infected but non-sporulent)
    Ifc = np.zeros((t,Lx,Ly))   # sporulent, actively infectious surface I
    Ifv = np.zeros((t,Lx,Ly))   # symptomatic surface I^{vid} (who went through state I, and eventually dead)
    Rem = np.zeros((t,Lx,Ly))   # senescent R surface
    LAI = np.zeros((t,Lx,Ly))   # total canopy surface
    LAI_alive = np.zeros((t,Lx,Ly)) # total wheat surface alive (Sus+Lat+Ifc)
    LAI_wheat = np.zeros((t,Lx,Ly)) # total wheat surface (Sus+Lat+Ifc+Rem)
    Poo = np.zeros((t,Lx,Ly))   # spore reservoir P, in fields/plots
    Eps = np.zeros((t,Lx,Ly))   # spore proportion intercepted by the canopy
    F_wheat_d = np.zeros((t,Lx,Ly)) # Spore fraction intercepted by wheat dominant
    F_comp_s = np.zeros((t,Lx,Ly)) # Spore fraction intercepted by companion under
    F_comp_d = np.zeros((t,Lx,Ly))  # Spore fraction intercepted by companion dominant
    F_wheat_s = np.zeros((t,Lx,Ly))  # Spore fraction intercepted by wheat under
    F_wheat = np.zeros((t,Lx,Ly)) # Spore fraction intercepted by wheat
    F_comp = np.zeros((t,Lx,Ly)) # Spore fraction intercepted by companion
    AUDPC = np.zeros((t,Lx,Ly)) # epidemic severity (Ifv integral)(Area Under Disease Progression Curve)
    Nsp = np.zeros((t,Lx,Ly))   # Number of spores available to infect the canopy
    Scont = np.zeros((t,Lx,Ly)) # healthy canopy surface who just got infected
    Ex = np.zeros((t,Lx,Ly)) # canopy fraction intercepting spores

    ### initialisation of LAI_K_ble and LAI_K_pois
    LAI_K_ble = 0.0
    #LAI_K_pois = 0.0

    ### staggering parameter, path E --> I
    g_pre = np.concatenate([np.zeros((lambd-delta_ei-1)), np.arange( (1.0/(2*delta_ei+1)), 1+(1.0/(2*delta_ei+1)), (1.0/(2*delta_ei+1)) )])
    g = np.reshape(g_pre, (lambd+delta_ei, 1, 1)) * np.ones((lambd + delta_ei, 1, 1))


    ### MAIN FUNCTION
    for i in range(0, t):
        # Function initialisation
        if np.mod(i, season) == 0:
            ### ble = matrix (Lx, Ly), represents the wheat proportion in landscape fields
            ### ex: [0 0 0 ; 1 1 1 ; 0.5 0.5 0.5] represents one landscape
            ### 1st row of fields: cropped without wheat; 2nd: wheat only; 3rd: mix with 50% of wheat
            res_frac = arrangement[int((np.floor(i / season) % Lr)), :, :]
            LAI_K_ble = res_frac * LAI_K
            #LAI_K_pois = (1 - res_frac) * LAI_K  # If we suppose that LAI of wheat and the companion species are equivalent

            ### Canopy initialisation
            sth0 = LAI_K_ble / 1000.0
            #pth0 = LAI_K_pois / 1000.0

            ### INITIALISATION OF STATE VARIABLES
            Eta = np.zeros((lambd + delta_ei, Lx, Ly))
            Nsp[i, :, :] = 0 * np.ones((Lx, Ly))
            #Pth[i, :, :] = pth0 * np.ones((Lx, Ly))
            #Poi[i, :, :] = pth0 * np.ones((Lx, Ly))
            if delta_companion == 0:
                Pth[i, :, :] = Pth_inde[0,:,:]
                Poi[i, :, :] = Poi_inde[0,:,:]
            elif delta_companion < 0:
                Pth[i, :, :] = Pth_inde[abs(delta_companion),:,:]
                Poi[i, :, :] = Poi_inde[abs(delta_companion),:,:]
            else:
                if i < delta_companion:
                    Pth[i, :, :] = 0 * np.ones((Lx, Ly))
                    Poi[i, :, :] = 0 * np.ones((Lx, Ly))
                else:
                    Pth[i, :, :] = Pth_inde[-1-delta_companion, :, :]
                    Poi[i, :, :] = Poi_inde[-1-delta_companion, :, :]
            Sth[i, :, :] = sth0 * np.ones((Lx, Ly))
            Sus[i, :, :] = sth0 * np.ones((Lx, Ly))
            Lat[i, :, :] = 0 * np.ones((Lx, Ly))
            Ifc[i, :, :] = 0 * np.ones((Lx, Ly))
            Ifv[i, :, :] = 0 * np.ones((Lx, Ly))
            Rem[i, :, :] = 0 * np.ones((Lx, Ly))
            LAI[i, :, :] = Sus[i, :, :] + Lat[i, :, :] + Ifc[i, :, :] + Rem[i, :, :] + Pth[i, :, :]
            LAI_alive[i, :, :] = Sus[i, :, :] + Lat[i, :, :] + Ifc[i, :, :]
            LAI_wheat[i, :, :] = Sus[i, :, :] + Lat[i, :, :] + Ifc[i, :, :] + Rem[i, :, :]
            if i != 0 and theta != 0: # theta = 0.01
                if disease == 'rust':
                    Poo[i, :, :] = theta * (Poo[i - 1, :, :] + sigma * Ifc[i - 1, :, :])
                if disease == 'septo':
                    Poo[i, :, :] = theta * (Poo[i - 1, :, :] + (sigma + sigma_asco) * Ifc[i - 1, :, :])
            else:
                Poo[i, :, :] = inoc_init * np.ones((Lx, Ly))
            if h_wheat == 0:
                Eps[i, :, :] = 1 - np.exp(-ber_wheat*LAI_alive[i, :, :] - ber_companion*Poi[i, :, :])
            else:
                DomFac_wheat = h_wheat / (h_wheat + h_companion)  # wheat dominance factor
                DomFac_comp = h_companion / (h_wheat + h_companion)  # wheat dominance factor
                F_wheat_d[i,:,:] = 1 - np.exp(-ber_wheat * LAI_alive[i,:,:])  # wheat dominant
                F_comp_s[i,:,:] = np.exp(-ber_wheat * LAI_alive[i,:,:]) * (1 - np.exp(-ber_companion * Poi[i,:,:]))  # companion under
                F_comp_d[i,:,:] = 1 - np.exp(-ber_companion * Poi[i,:,:])  # companion dominant
                F_wheat_s[i,:,:] = np.exp(-ber_companion * Poi[i,:,:]) * (1 - np.exp(-ber_wheat * LAI_alive[i,:,:]))  # wheat under
                F_wheat[i,:,:] = F_wheat_s[i,:,:] + DomFac_wheat * (F_wheat_d[i,:,:] - F_wheat_s[i,:,:])
                F_comp[i,:,:] = F_comp_s[i,:,:] + DomFac_comp * (F_comp_d[i,:,:] - F_comp_s[i,:,:])
                Eps[i,:,:] = F_wheat[i,:,:] + F_comp[i,:,:]
            AUDPC[i, :, :] = 0 * np.ones((Lx, Ly))
            Scont[i, :, :] = 0 * np.ones((Lx, Ly))
            Ex[i, :, :] = 0 * np.ones((Lx, Ly))

        # Main function after initialisation
        else:
            pluie = np.mod(i, season) in rain[:, np.mod(int(np.floor(i/season)), rain.shape[1])] #pour les évènement de dispersion de la septo

            pth = Pth[i-1, :, :]
            poi = Poi_inde[i-1, :, :]
            sth = Sth[i-1, :, :]
            sus = Sus[i-1, :, :]
            lat = Lat[i-1, :, :]
            ifc = Ifc[i-1, :, :]
            ifv = Ifv[i-1, :, :]
            rem = Rem[i-1, :, :]
            poo = Poo[i-1, :, :]
            lai = LAI[i-1, :, :]
            lai_alive = LAI_alive[i-1, :, :]
            lai_wheat = LAI_wheat[i-1, :, :]
            eta = Eta
            nsp = Nsp[i-1, :, :]
            audpc = AUDPC[i-1, :, :]

            ### SPORE POOL: production and dispersion at the field-level
            # (for septoriose, this takes also into account ascospores coming from the fields)
            ng_field_asco = 0
            ng_field_pycnid = 0
            ng_field_ure = 0
            if disease == "septo":
                #ascospores
                if ((i % season) % (2*int(delta_t0/delta_t))) == 0:  # ascospore dispersion every 20 dd (explaining the 2 modulus)
                    ng_field_asco = ndimage.convolve(ifc * sigma_asco, kernel_asco, mode='mirror')
                #pycnidiospores
                if pluie == 1:  # pycnidiospore dispersion during rain events
                    ng_field_pycnid = ndimage.convolve(ifc * sigma, kernel_pycnid, mode='mirror')
            elif disease == "rust":
                #urediospores
                if ((i % season) % (2*int(delta_t0/delta_t))) == 0:  # urediospore dispersion every 20 dd (explaining the 2 modulus)
                    ng_field_ure = ndimage.convolve(ifc * sigma, kernel_ure, mode='mirror')

            ### SPORE POOL: Soil inoculum (Poo remobilisation)
            if disease == "septo":
                inoc = max(0,(1-np.mod(i,season)/(70*int(delta_t0/delta_t)))) * poo * (np.mod(i,season) >= inf_begin) * pluie
                #spores_parcelle = sigma * ifc * pluie
            elif disease == "rust":
                inoc = poo * (np.mod(i, season) >= inf_begin)
                #spores_parcelle = (1 - alpha) * sigma * ifc * (np.mod(np.mod(i, season), 2*int(delta_t0/delta_t)) == 0)

            ### SPORE POOL: External cloud infecting the field
            if ((i % season) % (2 * int(delta_t0 / delta_t))) == 0:
                #if isinstance(ng_ext0, int) == 1:
                if disease == 'rust':
                    ng_ext = ng_ext0 * (np.mod(i, season) >= inf_begin and #i < season and
                                        np.mod(i, season) < (20*int(delta_t0/delta_t) + inf_begin))
                if disease == 'septo':
                    ng_ext = ng_ext0 * (np.mod(i, season) >= inf_begin and
                                        np.mod(i, season) < (20 * int(delta_t0 / delta_t) + inf_begin))
                # else:
                #     ng_ext = ng_ext0[np.mod(int(np.floor(i / season)), ng_ext0.shape[0]), :, :] * (
                #             np.mod(i, season) >= inf_begin and
                #             np.mod(i, season) < (20*int(delta_t0/delta_t) + inf_begin))
            else:
                ng_ext = 0

            ### TOTAL SPORE POOL
            if disease == 'septo':
                nsp = inoc + ng_ext + ng_field_asco + ng_field_pycnid  # + spores_parcelle
            if disease == 'rust':
                nsp = inoc + ng_ext + ng_field_ure  # + spores_parcelle

            ### SPORE INTERCEPTION by healthy canopy (Poisson Law)
            eps = Eps[i - 1, :, :]
            if h_wheat == 0: #without ERIN
                if ber_companion == 0:
                    fac_int_wheat = 1
                else:
                    fac_int_wheat = (ber_wheat * lai_alive) / (ber_wheat * lai_alive + ber_companion * poi)
                    fac_int_comp = 1 - fac_int_wheat
                if 0 in lai_alive:
                    ex = np.zeros((Lx,Ly))
                    for j in range(0,Lx):
                        for k in range (0, Ly):
                            if lai_alive[j,k]==0:
                                ex[j,k] = 1
                            else:
                                ex[j,k] = np.exp(-(fac_int_wheat[j,k] * eps[j,k] * pi_inf0 * nsp[j,k] * s0/lai_alive[j,k]))
                else:
                    ex = np.exp(-(fac_int_wheat * eps * pi_inf0 * nsp * s0 / lai_alive))
            else: # with ERIN
                f_wheat = F_wheat[i - 1, :, :]
                if 0 in lai_alive:
                    ex = np.zeros((Lx,Ly))
                    for j in range(0,Lx):
                        for k in range (0, Ly):
                            if lai_alive[j,k]==0:
                                ex[j,k] = 1
                            else:
                                ex[j,k] = np.exp(-(f_wheat[j,k] * pi_inf0 * nsp[j,k] * s0/lai_alive[j,k]))
                else:
                    ex = np.exp(-(f_wheat * pi_inf0 * nsp * s0 / lai_alive))

            ### Canopy fraction intercepting spores
            Ex[i,:,:] = ex
            ### Healthy surface contaminated
            Sc = (1 - ex) * sus


            ### Crop growth
            crS = beta_wheat * (sth) * (1 - sth / (LAI_K_ble + (LAI_K_ble == 0))) * (np.mod(i, season) < end_wheat)
            #crP = beta_companion * (pth) * (1 - pth / (LAI_K_pois + (LAI_K_pois == 0))) * (np.mod(i, season) < end_companion)

            ### COMPUTING STATE VARIABLES
            #Pth[i,:,:] = pth + crP
            #Poi[i,:,:] = poi + crP - mu * poi * (np.mod(i,season) >= end_companion)
            if delta_companion < 0:
                if abs(delta_companion)+np.mod(i, season) < season:
                    Pth[i, :, :] = Pth_inde[abs(delta_companion)+i, :, :]
                    Poi[i, :, :] = Poi_inde[abs(delta_companion)+i, :, :]
                else:
                    Pth[i, :, :] = Pth_inde[-season+ abs(delta_companion) + i, :, :]
                    Poi[i, :, :] = Poi_inde[-season+ abs(delta_companion) + i, :, :]
            else:
                if i < delta_companion :
                    Pth[i, :, :] = np.zeros((Lx,Ly))
                    Poi[i, :, :] = np.zeros((Lx,Ly))
                else:
                    Pth[i, :, :] = Pth_inde[int(i-delta_companion), :, :]
                    Poi[i, :, :] = Poi_inde[int(i-delta_companion), :, :]
            Sth[i,:,:] = sth + crS - mu_wheat * sth * (np.mod(i, season) >= end_wheat)
            Sus[i,:,:] = np.maximum(0, sus + crS * pow(((sus+lat)/(sth+(sth==0))),gamma) - Sc - mu_wheat*sus*(np.mod(i,season)>=end_wheat))

            Eta[1:lambd+delta_ei,:,:] = eta[0:-1,:,:] * (1 - g[0:-1,:,:])
            Eta[0,:,:] = Sc
            Eta = (1 - mu_wheat * (np.mod(i, season) >= end_wheat)) * Eta
            Lat[i,:,:] = Eta.sum(axis=0)

            if disease == "septo":
                Ifc[i, :, :] = ifc * (1 - psi * pluie) - nu * ifc + np.sum((eta * g), axis=0)
                Rem[i,:,:] = rem + ifc * psi * pluie + np.sum((mu_wheat * Eta * (np.mod(i, season) >= end_wheat)), axis=0) + mu_wheat * sus * (
                            np.mod(i, season) >= end_wheat) + nu * ifc
            elif disease == "rust":
                Ifc[i,:,:] = ifc - nu * ifc + np.sum((eta * g), axis=0)
                Rem[i,:,:] = rem + np.sum(mu_wheat * Eta * (np.mod(i, season) >= end_wheat), axis=0) + mu_wheat * sus * (
                            np.mod(i, season) >= end_wheat) + nu * ifc

            Ifv[i,:,:] = ifv + np.sum((eta * g), axis=0)
            LAI[i,:,:] = Sus[i,:,:] + Lat[i,:,:] + Ifc[i,:,:] + Rem[i,:,:] + Pth[i,:,:]
            LAI_alive[i, :, :] = Sus[i, :, :] + Lat[i, :, :] + Ifc[i, :, :]
            LAI_wheat[i, :, :] = Sus[i, :, :] + Lat[i, :, :] + Ifc[i, :, :] + Rem[i, :, :]
            Poo[i, :, :] = poo - inoc + (1 - eps) * nsp + (1 - pi_inf0) * eps * nsp - rho * poo # BE CAREFUL EPS vs F_wheat
            AUDPC[i,:,:] = audpc + Ifv[i,:,:]
            Nsp[i,:,:] = nsp
            # if ber_companion == 0:
            #     Eps[i,:,:] = 1 - np.exp(-ber_wheat*LAI[i,:,:])
            # else:
            if h_wheat == 0:
                Eps[i,:,:] = 1 - np.exp((-ber_wheat*LAI_alive[i,:,:]) -(ber_companion*Poi[i,:,:]))
            else:
                DomFac_wheat = h_wheat / (h_wheat + h_companion)  # wheat dominance factor
                DomFac_comp = h_companion / (h_wheat + h_companion)  # wheat dominance factor
                F_wheat_d[i,:,:] = 1 - np.exp(-ber_wheat * LAI_alive[i,:,:])  # wheat dominant
                F_comp_s[i,:,:] = np.exp(-ber_wheat * LAI_alive[i,:,:]) * (1 - np.exp(-ber_companion * Poi[i,:,:]))  # companion under
                F_comp_d[i,:,:] = 1 - np.exp(-ber_companion * Poi[i,:,:])  # companion dominant
                F_wheat_s[i,:,:] = np.exp(-ber_companion * Poi[i,:,:]) * (1 - np.exp(-ber_wheat * LAI_alive[i,:,:]))  # wheat under
                F_wheat[i,:,:] = F_wheat_s[i,:,:] + DomFac_wheat * (F_wheat_d[i,:,:] - F_wheat_s[i,:,:])
                F_comp[i,:,:] = F_comp_s[i,:,:] + DomFac_comp * (F_comp_d[i,:,:] - F_comp_s[i,:,:])
                Eps[i,:,:] = F_wheat[i,:,:] + F_comp[i,:,:]
            Scont[i,:,:] = Sc

    return Nsp, Pth, Poi, Sth, Sus, Lat, Ifc, Ifv, Rem, LAI, LAI_wheat, Poo, Eps, AUDPC, Scont
