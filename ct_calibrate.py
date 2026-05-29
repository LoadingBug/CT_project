import numpy as np
import scipy
from scipy import interpolate
from ct_phantom import ct_phantom
from ct_scan import ct_scan
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
    
    sinogram_air = np.mean(sinogram_air[0])

<<<<<<< HEAD
	# Get dimensions and work out detection for just air of twice the side
	# length (has to be the same as in ct_scan.py)
	n = sinogram.shape[1]
	phantom = ct_phantom(material.name, n, 1, 'Air')
	sinogram_air = ct_scan(photons, material, phantom, scale, 1)
	sinogram_air = np.mean(sinogram_air[0])
=======
    sinogram_ratio = np.maximum(sinogram / sinogram_air, 1e-10)
    p_m = -np.log(sinogram_ratio)
>>>>>>> chloely

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
    t_w_m = f_interp(p_m)

    C = p_w[1] / t_w[1]

    # Calculate the final calibrated attenuation
    sinogram_calibrated = C * t_w_m

    return sinogram_calibrated

# def ct_calibrate(photons, material, sinogram, scale, correct_beam_hardening=False):

# 	""" ct_calibrate convert CT detections to linearised attenuation
# 	sinogram = ct_calibrate(photons, material, sinogram, scale) takes the CT detection sinogram
# 	in x (angles x samples) and returns a linear attenuation sinogram
# 	(angles x samples). photons is the source energy distribution, material is the
# 	material structure containing names, linear attenuation coefficients and
# 	energies in mev, and scale is the size of each pixel in x, in cm."""

# 	# Get dimensions and work out detection for just air of twice the side
# 	# length (has to be the same as in ct_scan.py)
# 	n = sinogram.shape[1]
# 	phantom = ct_phantom(material.name, n, 1, 'Air')
# 	sinogram_air = ct_scan(photons, material, phantom, scale, 1)
	
# 	sinogram_air = np.mean(sinogram_air[0])

# 	# Perform calibration
# 	sinogram_ratio = np.maximum(sinogram / sinogram_air, 1e-10)
# 	p_m = -np.log(sinogram_ratio)

# 	if not correct_beam_hardening:
# 		return p_m

# 	# Initialise water thickness values for calibration
# 	max_thickness = n * scale
# 	t_w = np.linspace(0, max_thickness, 100)
	
# 	# Use water to calibrate
# 	I_0 = ct_detect(photons, material.coeff('Water'), np.array([0.0]))[0]
# 	I = ct_detect(photons, material.coeff('Water'), t_w)
    
#     # Attenuation for water measured as usual (without beam hardening correction)
# 	p_w = -np.log(np.maximum(I / I_0, 1e-10))
    
# 	f = interpolate.interp1d(p_w, t_w, bounds_error=False, fill_value="extrapolate")
        
#     # Calculate expected equivalent water thickness using interpolated function of material attenuation values
# 	t_wm = f(p_m)
    
#     # Calculate scaling factor by fitting constant function to datapoints C = p/t_{w,m}
# 	C = p_m[1] / t_wm[1]
    
#     # Scale for beam hardening corrected attenuation
# 	sinogram_calibrated = C * t_wm

# 	return sinogram_calibrated