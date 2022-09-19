import os
import numpy as np
import math


from epyland.f_rain import f_rain ## f_rain
from epyland.inoculum import inoculum ## inoculum
from epyland.f_rotation import f_rotation ## f_rotation
from epyland.SEIR3 import SEIR ## SEIR fonction principale

### IMPORTATION DES FONCTIONS

parameters = dict(

    ### Parametres generaux (renseignes dans WRL/STB)
    mu=0.03,  # 0.03 %% mortalite des tissus S et E
    nu=0.03,  # nu = mu %% mortalite des tissus infectieux I
    beta_ble=0.09,  # 0.09 %% parametre de croissance du ble
    beta_pois=0.09,  # beta_pois = beta_ble %% parametre de croissance du pois
    s0=0.0001,  # 0.0001 %% taille d'une lesion
    Cr_ble=140,  # 1400 dj %% date de fin de la croissance du ble
    Cr_pois=140,  # Cr_pois = Cr_ble %% date de fin de la croissance du pois
    pi_inf0=0.0002,  # 0.0002 %% probabilite d'infection d'une spore
    LAIpot=6,  # 6 %% capacite de charge (LAI maximal du couvert)
    ng_ext0_abs=20000,  # 20000 %% spores arrivant via un nuage exterieur au paysage
    ber=1,  # 1 # coeff d'interception des spores (il s'agit d'une loi de Beer-Lambert)
    inoc_init_abs=500000,  # 500000 %% spores presentes initialement dans le reservoir P
    # uniquement utilise dans le scenario d'inoculation d'un focus central

    ### Parametres specifiques (renseignes dans WRL/STB)
    maladie="septo",
    alpha=0.5,  # 0.5 %% fraction des spores sortant de la parcelle
    rho=0.01,  # 0.01 %% mortalite des spores du reservoir P
    psi=0.0,  # 0 %% taux de vidage des pycnides (seulement pour la septoriose)
    gamma=0,  # 0 %% parametre de virulence
    lambd=10,  # 100 dj %% latence
    theta=0.01,  # 0.01 %% taux de survie interculturale des spores
    sigma=1500000,  # 1500000 %% taux de production de spores
    sigma_asco=0,  # 0 %% (parametre pertinent pour la septoriose uniquement)
    rda=5,  # 5 %% rayon de dispersion
    inf_begin=100  # 1000 dj %% date de debut de l'epidemie (typiquement comprise entre 80 et 130 pour la rouille)
)

## Taille de la parcelle
Lx = 21
Ly = 21

### f_rain
annees = [1994, 1995]
rain = f_rain(annees)



############
############ TEST SIMPLE SEIR
############

## Paramètres d'entrée
t = 250
saison = 250  # 2500 dj %% longueur d'une saison culturale
inoc_init = 0  # pour fonction init_saison

##Scenario de rotation (Lx,Ly,Lr)
rotation = np.ones((2, 2, 2))
#rotation[2,1,1]=1

### fonction SEIR
[Nsp, Pth, Poi, Sth, Sus, Lat, Ifc, Ifv, Rem, LAI, Poo, Eps, AUDPC, Scont] = SEIR(ng_ext0=parameters['ng_ext0_abs'],rain=rain,inoc_init=inoc_init,rotation=rotation,t=t,saison=saison,**parameters)
print(Sth)





############
############ SEIR + PROPORTION DU COUVERT INFECTE OU RESERVOIR DE SPORES
############

# t = 1000
# T = [*range(0,t)]
# Lx = 1
# Ly = Lx
# rotation = np.ones((1,Lx,Ly))
#
# [inoc_init, ng_ext0] = inoculum("nuage annuel",1)
# [Nsp, Pth, Poi, Sth, Sus, Lat, Ifc, Ifv, Rem, LAI, Poo, Eps, AUDPC, Scont] = SEIR(lambd,theta,sigma,sigma_asco,rda,pi_inf0,LAIpot,ng_ext0,inf_begin,ber,rain,inoc_init,rotation,t)
# print(Sth)


############
############ SCENARIOS DE ROTATION
############

# sc = "R3ans-synchrone-67%ble"
# rotation = f_rotation(3,sc,1,1)
# inoc_init = inoc_init_abs ## On demarre l'epidemie avec un inoculum present dans la parcelle (reservoir) la premiere annee
# ng_ext0 = 0 ## Pas de spores venant de l'exterieur de la parcelle
#
# t = 3000
# T = [*range(0,t)]
# [Nsp, Pth, Poi, Sth, Sus, Lat, Ifc, Ifv, Rem, LAI, Poo, Eps, AUDPC, Scont] = SEIR(lambd,theta,sigma,sigma_asco,rda,pi_inf0,LAIpot,ng_ext0,inf_begin,ber,rain,inoc_init,rotation,t)
