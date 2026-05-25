from ct_scan import *
from ct_calibrate import *
from ct_lib import *
from ramp_filter import *
from back_project import *
from hu import *

def scan_and_reconstruct(photons, material, phantom, scale, angles, mas=10000, alpha=0.001, scatterfrac = 0.0, backgroundrate = 0.0):

	""" Simulation of the CT scanning process
		reconstruction = scan_and_reconstruct(photons, material, phantom, scale, angles, mas, alpha)
		takes the phantom data in phantom (samples x samples), scans it using the
		source photons and material information given, as well as the scale (in cm),
		number of angles, time-current product in mas, and raised-cosine power
		alpha for filtering. The output reconstruction is the same size as phantom."""


	# convert source (photons per (mas, cm^2)) to photons
	photons = photons * mas * scale**2

	# model noise
	photons += scale **2 * np.random.poisson(scatterfrac * photons) # scatter noise
	photons += scale **2 * np.random.poisson(backgroundrate, size = photons.shape) # background noise

	# create sinogram from phantom data, with received detector values
	sinogram = ct_scan(photons, material, phantom, scale, angles)
	# convert detector values into calibrated attenuation values
	sinogram_attenuation = ct_calibrate(photons, material, sinogram, scale)
	# Ram-Lak
	fs = ramp_filter(sinogram_attenuation, scale, alpha)
	# Back-projection
	reconstruction = back_project(fs)
	# convert to Hounsfield Units
	reconstruction = hu(photons, material, reconstruction, scale)
	return reconstruction 