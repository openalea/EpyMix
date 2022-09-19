import os
import numpy as np
import math
from scipy.integrate import quad

### SPORE INTERCEPTION FUNCTION BY CANOPY
# def epsilon(ber_ble, LAI_ble, ber_pois, LAI_pois):
#     e = 1 - np.exp(-ber * S)
#     return e

def epsilon(ber_wheat, LAI_K):
    e = 1 - np.exp(-ber_wheat * LAI_K)
    return e


### FUNCTION FOR SPORE CLOUD DISPERSION INTO THE LANDSCAPE
def dispersion_kernel_septo(day_length, alpha_asco, radius_asco, alpha_pycnid, radius_pycnid):
    # Dispersion for ascospores
    def f(r):
        return pow(abs(r)+1,-alpha_asco)
    Disp_asco = []
    for i in range(-radius_asco, radius_asco+1):
        Disp_asco.append(quad(f, i - 0.5, i + 1 - 0.5)[0] / quad(f, -radius_asco-0.5, radius_asco+0.5)[0])
    Disp_asco = np.array(Disp_asco)
    kernel_asco = Disp_asco[:, np.newaxis] * Disp_asco[np.newaxis, :]
    C_Disp_asco = int(np.ceil(kernel_asco.shape[0] / 2.0))
    # Dispersion for pycnidiospres
    def f(r):
        return (1 / (4 * math.pi * alpha_pycnid * day_length)) * np.exp(-(pow(r, 2) / (4 * alpha_pycnid * day_length)))
    Disp_pycnid = []
    for i in range(-radius_pycnid, radius_pycnid+1):
        Disp_pycnid.append(quad(f, i - 0.5, i + 1 - 0.5)[0] / quad(f, -radius_pycnid-0.5, radius_pycnid+0.5)[0])
    Disp_pycnid = np.array(Disp_pycnid)
    kernel_pycnid = Disp_pycnid[:, np.newaxis] * Disp_pycnid[np.newaxis, :]
    C_Disp_pycnid = int(np.ceil(kernel_pycnid.shape[0] / 2.0))
    return kernel_asco, C_Disp_asco, kernel_pycnid, C_Disp_pycnid


def dispersion_kernel_rust(day_length, alpha_ure, radius_ure):
    def f(r):
        return pow(abs(r)+1,-alpha_ure)
    Disp_ure = []
    for i in range(-radius_ure, radius_ure+1):
        Disp_ure.append(quad(f, i - 0.5, i + 1 - 0.5)[0] / quad(f, -radius_ure-0.5, radius_ure+0.5)[0])
    Disp_ure = np.array(Disp_ure)
    kernel_ure = Disp_ure[:, np.newaxis] * Disp_ure[np.newaxis, :]
    C_Disp_ure = int(np.ceil(kernel_ure.shape[0] / 2.0))
    return kernel_ure, C_Disp_ure