import numpy as np
from attenuate import *
from ct_calibrate import *
from ct_detect import *

def hu(p, material, reconstruction, scale):
	""" convert CT reconstruction output to Hounsfield Units
	calibrated = hu(p, material, reconstruction, scale) converts the reconstruction into Hounsfield
	Units, using the material coefficients, photon energy p and scale given."""

	# use water to calibrate
	n = reconstruction.shape[1]
	thickness = n*scale
	I_0 = ct_detect(p, material.coeff('Water'), 0)
	I = ct_detect(p, material.coeff('Water'), thickness)

	# put this through the same calibration process as the normal CT data
	mu_w = -np.log(I / I_0) / thickness

	# use result to convert to hounsfield units
	hu_reconstruction = 1000 * (reconstruction - mu_w) / mu_w

	# limit minimum to -1024, which is normal for CT data.
	hu_reconstruction = np.maximum(hu_reconstruction, -1024)

	# limit maximum to +3027
	hu_reconstruction = np.minimum(hu_reconstruction, 3027)

	return hu_reconstruction