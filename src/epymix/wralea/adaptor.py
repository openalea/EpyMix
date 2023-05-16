import random

from openalea.core import *

from epymix.rain_WD import rain as _rain ## f_rain
from epymix.inoculum import inoculum ## inoculum
from epymix.configuration import configuration
from epymix.SEIR import SEIR ## SEIR fonction principale
from epymix.dispersion_gradient import dispersion_kernel_rust, dispersion_kernel_septo
from epymix.growth_companion import growth_pois as growth_pea


def rain(
        site='Landbruksmeteorologisk tjeneste', 
        time_start='2019-09-01', 
        time_end='2020-09-01', 
        delta_t=10, 
        sowing_date='2019-09-01', 
        rainfall_threshold=3):
    """ Rain or Precipitation from WeatherData"""
    return rain

def inoculum(
        scenario_ino = 'initial_inoculum',
        Lx=1,
        Ly=1,
        frac_inf = 1,
        inoc_init_abs = 20000000,
        ng_ext0_abs = 20000):
    """ Inoculum initialization """
    return inoc_init, ng_ext0

def configuration(
        Lr=1,
        Lx=1,
        Ly=1,
        scenario_rot='uniform',
        wheat_fraction=0.5):
    """ Set the spatial configutation/arrangement of th field """
    return arrangement

def dispersion_kernel_rust(
        day_length=4320,
        alpha_ure=3,
        radius_ure=5):
    """ Spore dispersion function for Rust """
    return kernel_ure, C_Disp_ure

def dispersion_kernel_septo(
        day_length=4320,
        alpha_asco=3,
        radius_asco=5,
        alpha_pycnid=2e-05,
        radius_pycnid=5):
    """ Spore dispersion function for Septoria """
    return kernel_ure, C_Disp_ure

def growth_pea(
        t=250,
        season=250,
        arrangement=arrangement,
        mu_companion=0.03,
        beta_companion=0.09,
        end_companion=140,
        LAI_K=6):
    """ Growth function for the companion species """
    return Pth_inde, Poi_inde

def SEIR(
        t=250,
        delta_t = 10,
        season=250,
        delta_companion=0,
        disease="septo",
        rain=rain,
        arrangement=arrangement,
        inoc_init=inoc_init,
        ng_ext0=ng_ext0,
        mu_wheat = 0.03,
        nu = 0.03,
        beta_wheat = 0.09,
        end_wheat = 140,
        LAI_K=6,
        ber_wheat=1,
        ber_companion=1,
        Pth_inde=Pth_inde,
        Poi_inde=Poi_inde,
        h_wheat=1,
        h_companion=1,
        lambd=20,
        delta_ei=5,
        s0=0.0001,
        pi_inf0=0.0002,
        rho=0.002,
        psi=0.3,
        gamma=0,
        theta=0.15,
        sigma=45000000,
        sigma_asco=9000000,
        inf_begin=0,
        C_Disp_ure=C_Disp_ure,
        kernel_ure=kernel_ure,
        C_Disp_asco=C_Disp_asco,
        kernel_asco=kernel_asco,
        C_Disp_pycnid=C_Disp_pycnid,
        kernel_pycnid=kernel_pycnid):
    """ Main function computing dynamic epidemics according to parameters  """
    return Nsp, Pth, Poi, Sth, Sus, Lat, Ifc, Ifv, Rem, LAI, LAI_wheat, Poo, Eps, AUDPC, Scont