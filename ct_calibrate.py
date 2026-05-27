import numpy as np
import scipy
from scipy import interpolate
from ct_phantom import ct_phantom
from ct_scan import ct_scan
from ct_detect import ct_detect

def ct_calibrate(photons, material, sinogram, scale, correct_beam_hardening=True):

	""" ct_calibrate convert CT detections to linearised attenuation
	sinogram = ct_calibrate(photons, material, sinogram, scale) takes the CT detection sinogram
	in x (angles x samples) and returns a linear attenuation sinogram
	(angles x samples). photons is the source energy distribution, material is the
	material structure containing names, linear attenuation coefficients and
	energies in mev, and scale is the size of each pixel in x, in cm."""

	# Get dimensions and work out detection for just air of twice the side
	# length (has to be the same as in ct_scan.py)
	n = sinogram.shape[1]
	phantom = ct_phantom(material.name, n, 1, 'Air')
	sinogram_air = ct_scan(photons, material, phantom, scale, 1)
	sinogram_air = sinogram_air[0][0]

	# Perform calibration
	sinogram = sinogram / sinogram_air
	p_m = -np.log(sinogram)

	if not correct_beam_hardening:
		return p_m

	# Initialise water thickness values for calibration
	n = sinogram.shape[1]
	max_thickness = n * scale
	t_w = np.linspace(0, max_thickness, 100)
	
	# Use water to calibrate
	I_0 = ct_detect(photons, material.coeff('Water'), 0)
	I = ct_detect(photons, material.coeff('Water'), t_w)
    
    # Attenuation for water measured as usual (without beam hardening correction)
	p_w = -np.log(np.maximum(I / I_0, 1e-10))
    
	f = interpolate.interp1d(p_w, t_w, kind='linear', bounds_error=False, fill_value="extrapolate")
        
    # Calculate expected equivalent water thickness using interpolated function of material attenuation values
	t_wm = f(p_m)
    
    # Calculate scaling factor by fitting constant function to datapoints C = p/t_{w,m}
	C = p_m[1] / t_wm[1]
    
    # Scale for beam hardening corrected attenuation
	p_m = C * t_wm

	return p_m