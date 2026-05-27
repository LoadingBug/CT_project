import numpy as np
import scipy
from scipy import interpolate
from ct_phantom import ct_phantom
from ct_scan import ct_scan

import numpy as np
import scipy
from scipy import interpolate
from ct_phantom import ct_phantom
from ct_scan import ct_scan
# Assuming ct_detect is available based on your reference snippet
from ct_detect import ct_detect 

def ct_calibrate(photons, material, sinogram, scale, correct_beam_hardening=True):
    """ 
    ct_calibrate convert CT detections to linearised attenuation
    sinogram = ct_calibrate(photons, material, sinogram, scale) takes the CT detection sinogram
    in x (angles x samples) and returns a linear attenuation sinogram (angles x samples). 
    photons is the source energy distribution, material is the material structure containing names, 
    linear attenuation coefficients and energies in mev, and scale is the size of each pixel in x, in cm.
    
    Includes an optional toggle for beam hardening correction based on water equivalence.
    """

    n = sinogram.shape[1]
    phantom = ct_phantom(material.name, n, 1, 'Air')
    sinogram_air = ct_scan(photons, material, phantom, scale, 1)
    
    sinogram_air = sinogram_air[0][0]

    sinogram_ratio = np.maximum(sinogram / sinogram_air, 1e-10)
    p_m = -np.log(sinogram_ratio)

    if not correct_beam_hardening:
        return p_m

    max_thickness = n * scale
    t_w = np.linspace(0, max_thickness, 100)
    
    water_coeffs = material.coeff('Water')

    I_w = ct_detect(photons, water_coeffs, t_w)
    I_0 = ct_detect(photons, water_coeffs, np.array([0.0]))[0]

    p_w = -np.log(np.maximum(I_w / I_0, 1e-10))

    # Fit a function t_w = f(p_w) using scipy's 1D interpolation
    f_interp = interpolate.interp1d(p_w, t_w, bounds_error=False, fill_value="extrapolate")

    # Apply the function to the measured data to find the equivalent water thickness
    t_w_m = f_interp(p_m)

    # Scale by C so that p approx p_m at a low thickness
    # We grab a small step from our interpolation data (index 1) to find the initial linear slope
    C = p_w[1] / t_w[1]

    # Calculate the final calibrated attenuation
    sinogram_calibrated = C * t_w_m

    return sinogram_calibrated