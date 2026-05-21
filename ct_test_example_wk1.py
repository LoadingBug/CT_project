
# these are the imports you are likely to need
import numpy as np
from material import *
from source import *
from fake_source import *
from ct_phantom import *
from ct_lib import *
from scan_and_reconstruct import *
from create_dicom import *

material = Material()
source = Source()

### basic ct of phantom 3 with soft tissue (aka no) implant
def test_reference():
	# This test shows a relatively accurate reconstruction of a hip through filtered backprojection with Ram-Lak filter, 
	# alpha = 0.1. The resolution is sufficient to capture all the detail of the hip image. 
	# There are noticeable beam hardening artifacts as streaks radiating from the bone (highly attenuating). 
	# The contrast clearly shows the different types of materials and these approximately match the linear attenuation coefficients for 50kVp, 
	# which is about the strength of the filtered source.
	
	M = ct_phantom(material.name, 256, 3,'Soft Tissue')
	ct = scan_and_reconstruct(source.photon('80kVp, 2mm Al'), material, M, 0.1, 256, alpha = 0.1)
	save_draw(ct, 'results/wk1', "test_reference", caxis = [0, None])

# print('Test reference')
# test_reference()

# default with titanium implant
def test_titanium():
	# There are much stronger beam hardening artifacts radiating from the titanium implant, 
	# as dark streaks with lower-energy photons filtered out. 
	# Titanium has a much higher linear attenuation coefficient at about 3.5 (matching the 60kVp value).

	M = ct_phantom(material.name, 256, 3,'Titanium')
	ct = scan_and_reconstruct(source.photon('80kVp, 2mm Al'), material, M, 0.1, 256, alpha = 0.1)
	save_draw(ct, 'results/wk1', "test_titanium", caxis = [0, None])

# print('Test titanium')
# test_titanium()


### default with scale 0.05 & 0.2
def test_scale():
	# At higher resolution (low scale), the maximum values are higher and the image looks slightly clearer, 
	# because we scale at more pixels.

	for i in [0.05, 0.2]:
		M = ct_phantom(material.name, 256, 3,'Soft Tissue')
		ct = scan_and_reconstruct(source.photon('80kVp, 2mm Al'), material, M, i,256, 0.1)
		save_draw(ct, 'results/wk1', f"test_phantom3_scale={i}.png", caxis = [0, None])
	
	for i in [0.05, 1, 0.2]:
		M = ct_phantom(material.name, 256, 8)
		ct = scan_and_reconstruct(source.photon('80kVp, 2mm Al'), material, M, i,256, 0.1)
		save_draw(ct, 'results/wk1', f"test_phantom8_scale={i}.png", caxis = [0, None])

print('Test scale')
test_scale()


### default with angle 128 & 512
def test_angle():
# Using fewer angles reduces the resolution of the reconstruction because the interpolation is done using less data values, 
# and reveals obvious pixelation. Using more angles increases the quantity of data and computation time but sharpens the image.
	
	for i in [128, 512]:
		M = ct_phantom(material.name, i, 3,'Soft Tissue')
		ct = scan_and_reconstruct(source.photon('80kVp, 2mm Al'), material, M, 0.1, i, alpha = 0.1)
		save_draw(ct, 'results/wk1', f"test_angle={i}.png", caxis = [0, None])

# print('Test angle')
# test_angle()


### default with alpha 0, 0.01, 1 & 2
def test_alpha():
# There is little observed change for the phantom when alpha changes 
# (except for alpha=0 which is likely an incompatibility with the code implementation) because it is generated with relatively low frequency. 
# We could expect a noisier, real scan to have its noise filtered out increasingly by the low-pass filter as alpha increases.

   for i in [0, 0.01, 1, 2]:
       M = ct_phantom(material.name, 256, 3,'Soft Tissue')
       ct = scan_and_reconstruct(source.photon('80kVp, 2mm Al'), material, M, 0.1, 256, i)
       save_draw(ct, 'results/wk1', f"test_alpha={i}.png", caxis = [0, None])

# print('Test alpha')
# test_alpha()


### default with source 80kVp - 1mm Al, 100kVp - 2mm Al & ideal fake source 0.08kVp
def test_source():
# As expected, a thinner filter gives stronger beam hardening artifacts; 
# a higher energy gives weaker beam hardening artifacts; and the ideal source gives no artifacts. 
# There doesn’t seem to be any change in the overall linear attenuation coefficients.

	sources = [source.photon('80kVp, 1mm Al'), source.photon('100kVp, 2mm Al'), fake_source(source.mev, 0.08, method='ideal')]
	for index, value in enumerate(sources):
		M = ct_phantom(material.name, 256, 3,'Soft Tissue')
		ct = scan_and_reconstruct(value, material, M, 0.1, 256, 0.1)
		save_draw(ct, 'results/wk1', f"test_source#{index}", caxis = [0, None])

# print('Test source')
# test_source()


### basic ct of phantom 5 and 8 with soft tissue
def test_phantom_type():

	for i in [4, 5, 6]:
		M = ct_phantom(material.name, 256, i,'Titanium')
		ct = scan_and_reconstruct(source.photon('80kVp, 2mm Al'), material, M, 0.1, 256, i)
		save_draw(ct, 'results/wk1', f"test_phantom_type={i}.png", caxis = [0, None])

# print('Test phantom type')
# test_phantom_type()