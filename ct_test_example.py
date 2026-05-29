
# these are the imports you are likely to need
import numpy as np
from material import *
from source import *
from fake_source import *
from ct_phantom import *
from ct_lib import *
from scan_and_reconstruct import *
from create_dicom import *

# create object instances
material = Material()
source = Source()

# define each end-to-end test here, including comments
# these are just some examples to get you started
# all the output should be saved in a 'results' directory

def test_1():
	# explain what this test is for

	# work out what the initial conditions should be
	p = ct_phantom(material.name, 256, 3)
	s = source.photon('100kVp, 3mm Al')
	y = scan_and_reconstruct(s, material, p, 0.01, 256)

	# save some meaningful results
	save_draw(y, 'results', 'test_1_image')
	save_draw(p, 'results', 'test_1_phantom')

	# how to check whether these results are actually correct?

def test_2():
	# explain what this test is for

	# work out what the initial conditions should be
	p = ct_phantom(material.name, 256, 2)
	s = source.photon('80kVp, 1mm Al')
	y = scan_and_reconstruct(s, material, p, 0.01, 256)

	# save some meaningful results
	save_plot(y[128,:], 'results', 'test_2_plot')

	# how to check whether these results are actually correct?

def test_3():
	# explain what this test is for

	# work out what the initial conditions should be
	p = ct_phantom(material.name, 256, 1)
	s = fake_source(source.mev, 0.1, method='ideal')
	y = scan_and_reconstruct(s, material, p, 0.1, 256)

	# save some meaningful results
	f = open('results/test_3_output.txt', mode='w')
	f.write('Mean value is ' + str(np.mean(y[64:192, 64:192])))
	f.close()

	# how to check whether these results are actually correct?

def test_4():
	# calibrated sinogram for phantom input 3 - single large hip replacement

    p = ct_phantom(material.name, 256, 3, 'Air')
    y = ct_scan(source.photon('100kVp, 2mm Al'), material, p, 0.1, 256)
    sinogram = ct_calibrate(source.photon('100kVp, 2mm Al'), material, y, 0.1)

    save_draw(sinogram, 'results', 'test_4_image')
    
def test_5():
	# scan_and_reconstruct test, alpha = 0

    M = ct_phantom(material.name, 256, 2,'Titanium')
    ct = scan_and_reconstruct(source.photon('80kVp, 2mm Al'), material, M, 0.1,256)
    
    save_draw(ct, 'results', 'test_5_image')

# Run the various tests
# print('Test 1')
# test_1()
# print('Test 2')
# test_2()
# print('Test 3')
# test_3()
# print('Test 4')
# test_4()
# print('Test 5')
# test_5()