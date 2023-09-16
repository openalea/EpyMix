import random

from openalea.core import *
import numpy as np
from epymix.rain_WD import rain as _rain ## f_rain
from epymix.inoculum import inoculum as _inoculum ## inoculum
from epymix.configuration import configuration as _configuration
from epymix.SEIR import SEIR as _SEIR ## SEIR fonction principale
from epymix.dispersion_gradient import dispersion_kernel_rust as _dispersion_kernel_rust 
from epymix.dispersion_gradient import dispersion_kernel_septo as _dispersion_kernel_septo 

from epymix.growth_companion import growth_pois


def rain(
        site='no.nibio.lmt' ,#'Landbruksmeteorologisk tjeneste' 
        time_start='2019-09-01', 
        time_end='2020-09-01', 
        delta_t=10, 
        sowing_date='2019-09-01', 
        rainfall_threshold=3):
    """ Rain or Precipitation from WeatherData"""
    return _rain(site=site, time_start=time_start, time_end=time_end, 
                 delta_t=delta_t, sowing_date=sowing_date ,rainfall_threshold=rainfall_threshold), 

def inoculum(
        scenario_ino = 'initial_inoculum',
        Lx=1,
        Ly=1,
        frac_inf = 1,
        inoc_init_abs = 20000000,
        ng_ext0_abs = 20000):
    """ Inoculum initialization """
    return _inoculum(scenario_ino,
                     Lx, Ly, frac_inf, inoc_init_abs, ng_ext0_abs)

def configuration(
        Lr=1,
        Lx=1,
        Ly=1,
        scenario_rot='uniform',
        wheat_fraction=0.5):
    """ Set the spatial configutation/arrangement of th field """
    return _configuration(Lr, Lx, Ly, scenario_rot, wheat_fraction),

def dispersion_kernel_rust(
        day_length=4320,
        alpha_ure=3,
        radius_ure=5):
    """ Spore dispersion function for Rust """
    return _dispersion_kernel_rust(day_length, alpha_ure, radius_ure)

def dispersion_kernel_septo(
        day_length=4320,
        alpha_asco=3,
        radius_asco=5,
        alpha_pycnid=2e-05,
        radius_pycnid=5):
    """ Spore dispersion function for Septoria """
    return _dispersion_kernel_septo(
        day_length,
        alpha_asco,
        radius_asco,
        alpha_pycnid,
        radius_pycnid)

def growth_pea(
        t=250,
        season=250,
        arrangement=None,
        mu_companion=0.03,
        beta_companion=0.09,
        end_companion=140,
        LAI_K=6):
    """ Growth function for the companion species """
    return growth_pois(
        t,
        season,
        arrangement,
        mu_companion,
        beta_companion,
        end_companion,
        LAI_K)

def SEIR(
        rain, arrangement, inoc_init, ng_ext0,Pth_inde, Poi_inde, 
        kernel_ure=[],
        C_Disp_ure=1,
        kernel_asco=[],
        C_Disp_asco=1,
        kernel_pycnid=[],
        C_Disp_pycnid=1,
        t=250,
        delta_t0 = 10,
        delta_t = 10,
        season=250,
        delta_companion=0,
        disease="septo",
        mu_wheat = 0.03,
        nu = 0.03,
        beta_wheat = 0.09,
        end_wheat = 140,
        LAI_K=6,
        ber_wheat=1,
        ber_companion=1,
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
):
    """ Main function computing dynamic epidemics according to parameters  """
    return _SEIR(
        t=t, 
        delta_t0=delta_t0, 
        delta_t=delta_t, 
        season=season, 
        delta_companion=delta_companion,
        disease=disease, 
        rain=rain, 
        arrangement=arrangement, 
        inoc_init=inoc_init, 
        ng_ext0=ng_ext0,
        mu_wheat=mu_wheat, 
        nu=nu, 
        beta_wheat=beta_wheat, #beta_companion=beta_companion, end_companion=end_companion
        end_wheat=end_wheat, 
        LAI_K=LAI_K, 
        ber_wheat=ber_wheat, 
        ber_companion=ber_companion, 
        Pth_inde=Pth_inde, 
        Poi_inde=Poi_inde,
        h_wheat=h_wheat, 
        h_companion=h_companion,
        lambd=lambd, 
        delta_ei=delta_ei,
        s0=s0,pi_inf0=pi_inf0, rho=rho, psi=psi, gamma=gamma, theta=theta, sigma=sigma, sigma_asco=sigma_asco, inf_begin=inf_begin,
        C_Disp_ure=C_Disp_ure, kernel_ure=kernel_ure, C_Disp_asco=C_Disp_asco, kernel_asco=kernel_asco,
        C_Disp_pycnid=C_Disp_pycnid, kernel_pycnid=kernel_pycnid
)



def ipm_SEIR(sowing_date='2019-09-01',
             daily_tmin=[10]*60,
             daily_tmax=[20]*60,
             daily_rain=[1]*30+[5]*30,
             delta_t=10,
             rainfall_threshold=3,
             scenario_ino='initial_inoculum',
             Lx=1,
             Ly=1,
             Lr=1,
             frac_inf=1,
             inoc_init_abs=20000000,
             ng_ext0_abs=20000,
             scenario_rot='uniform',
             wheat_fraction=0.5,
             day_length=4320,
             alpha_ure=3,
             radius_ure=5,
             alpha_asco=3,
             radius_asco=5,
             alpha_pycnid=2e-05,
             radius_pycnid=5,
             t=250,
             season=250,
             mu_companion=0.03,
             beta_companion=0.09,
             end_companion=140,
             LAI_K=6,
             delta_companion=0,
             disease="septo",
             mu_wheat=0.03,
             nu=0.03,
             beta_wheat=0.09,
             end_wheat=140,
             ber_wheat=1,
             ber_companion=1,
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
             inf_begin=0
             ) :
    daily_tmax = np.array(daily_tmax)
    daily_tmin = np.array(daily_tmin)
    daily_rain = np.array(daily_rain)
    daily_rain = np.where(daily_rain > rainfall_threshold, daily_rain, 0)
    dd = np.cumsum((daily_tmin + daily_tmax) / 2)
    dd_rain_days = np.ceil(dd[np.argwhere(daily_rain > 0)] / delta_t)
    inoc_init, ng_ext0 = inoculum(scenario_ino=scenario_ino,
                                  Lx=Lx,
                                  Ly=Ly,
                                  frac_inf=frac_inf,
                                  inoc_init_abs=inoc_init_abs,
                                  ng_ext0_abs=ng_ext0_abs)
    arrangement = configuration(Lr=Lr,
                                Lx=Lx,
                                Ly=Ly,
                                scenario_rot=scenario_rot,
                                wheat_fraction=wheat_fraction,
                                )[0]
    kernel_ure, C_Disp_ure = dispersion_kernel_rust(
        day_length=day_length,
        alpha_ure=alpha_ure,
        radius_ure=radius_ure)

    kernel_asco, C_Disp_asco, kernel_pycnid, C_Disp_pycnid = dispersion_kernel_septo(
        day_length=day_length,
        alpha_asco=alpha_asco,
        radius_asco=radius_asco,
        alpha_pycnid=alpha_pycnid,
        radius_pycnid=radius_pycnid)

    Pth_inde, Poi_inde = growth_pea(
        t=t,
        season=season,
        arrangement=arrangement,
        mu_companion=mu_companion,
        beta_companion=beta_companion,
        end_companion=end_companion,
        LAI_K=LAI_K)

    return SEIR(
        dd_rain_days, arrangement, inoc_init, ng_ext0, Pth_inde, Poi_inde,
        kernel_ure=kernel_ure,
        C_Disp_ure=C_Disp_ure,
        kernel_asco=kernel_asco,
        C_Disp_asco=C_Disp_asco,
        kernel_pycnid=kernel_pycnid,
        C_Disp_pycnid=C_Disp_pycnid,
        t=t,
        delta_t0=delta_t,
        delta_t=delta_t,
        season=season,
        delta_companion=delta_companion,
        disease=disease,
        mu_wheat=mu_wheat,
        nu=nu,
        beta_wheat=beta_wheat,
        end_wheat=end_wheat,
        LAI_K=LAI_K,
        ber_wheat=ber_wheat,
        ber_companion=ber_companion,
        h_wheat=h_wheat,
        h_companion=h_companion,
        lambd=lambd,
        delta_ei=delta_ei,
        s0=s0,
        pi_inf0=pi_inf0,
        rho=rho,
        psi=psi,
        gamma=gamma,
        theta=theta,
        sigma=sigma,
        sigma_asco=sigma_asco,
        inf_begin=inf_begin)