import math
import numpy as np
import numpy.matlib

def ramp_filter(sinogram, scale, alpha=0.001):
	""" Ram-Lak filter with raised-cosine for CT reconstruction

	fs = ramp_filter(sinogram, scale) filters the input in sinogram (angles x samples)
	using a Ram-Lak filter.

	fs = ramp_filter(sinogram, scale, alpha) can be used to modify the Ram-Lak filter by a
	cosine raised to the power given by alpha."""

	# get input dimensions
	angles = sinogram.shape[0]
	n = sinogram.shape[1]

	# set up filter to be at least twice as long as input
	m = np.ceil(np.log(2*n-1) / np.log(2))
	m = int(2 ** m)

	freqs = np.fft.fftfreq(m)
	ramp = np.abs(freqs)

	# cosine window
	cosine_window = np.ones(m)
	cosine_window[1:] = np.cos(freqs[1:] * np.pi) ** alpha
	filter_response = ramp * cosine_window / scale
	filter_response[0] = filter_response[1] / 6.0

	# apply filter to all angles
	print('Ramp filtering')

	sino_fft = np.fft.fft(sinogram, m)
	filtered_sino_fft = sino_fft * filter_response

	filtered_sinogram = np.fft.ifft(filtered_sino_fft).real
	filtered_sinogram = filtered_sinogram[:, :n]
	
	return filtered_sinogram
