import matplotlib.pyplot as plt
import numpy as np
import numpy.matlib
import os

def draw(data, map='gray', caxis=None):
	"""Draw an image"""
	create_figure(data, map, caxis)
	plt.show()

def draw_explicit_window(data, c, w, map='gray'):
    """Draw an image by explicitly applying the brightness function to the array."""
    
    # Apply the brightness formula
    windowed_data = 128 * (data - c) / w + 128
    
    # Clip values outside the 0-255 brightness range so they don't loop or overflow
    windowed_data = np.clip(windowed_data, 0, 255)
    
    # Draw the data (caxis is fixed to 0-255 since we already scaled the data)
    create_figure(windowed_data, map, caxis=[0, 255])
    plt.show()
	
def plot(data, x=None, title=None, xlabel=None, ylabel=None, xlim=None, ylim=None):
	"""plot a graph"""
	if x is None:
		plt.plot(data)
	else:
		plt.plot(x, data)
	if title is not None:
		plt.title( title )
	if xlabel is not None:
		plt.xlabel( xlabel )
	if ylabel is not None:
		plt.ylabel( ylabel )
	if xlim is not None:
		plt.xlim( xlim[0], xlim[1] )
	if ylim is not None:
		plt.ylim( ylim[0], ylim[1] )
	plt.show()

def save_draw(data, storage_directory, file_name, map='gray', caxis=None, title=None):
	"""save an image"""
	create_figure(data, map, caxis, title)
	full_path = get_full_path(storage_directory, file_name)
	plt.savefig(full_path)
	plt.close()

def save_plot(data, storage_directory, file_name, x=None, title=None, xlabel=None, ylabel=None, xlim=None, ylim=None):
	"""save a graph"""
	full_path = get_full_path(storage_directory, file_name)
 
	if x is None:
		plt.plot(data)
	else:
		plt.plot(x, data)
	if title is not None:
		plt.title( title )
	if xlabel is not None:
		plt.xlabel( xlabel )
	if ylabel is not None:
		plt.ylabel( ylabel )
	if xlim is not None:
		plt.xlim( xlim[0], xlim[1] )
	if ylim is not None:
		plt.ylim( ylim[0], ylim[1] )

	plt.savefig(full_path)
	plt.close()

def save_numpy_array(data, storage_directory, file_name):
	"""save a numpy array in .npy format"""

	full_path = get_full_path(storage_directory, file_name)

	np.save(full_path, data)

def load_numpy_array(storage_directory, file_name):
	"""load a .npy file into numpy array"""

	full_path = os.path.join(storage_directory, file_name)

	#add .npy extension if needed
	if not full_path.endswith('.npy'):
		full_path = full_path + '.npy'

	if not os.path.exists(full_path):
		raise Exception('File named ' + full_path + ' does not exist')

	return np.load(full_path)

def get_full_path(storage_directory, file_name):
	#create storage_directory if needed
	if not os.path.exists(storage_directory):
		os.makedirs(storage_directory)

	full_path = os.path.join(storage_directory, file_name)

	return full_path

def create_figure(data, map, caxis=None, title=None):
	fig, ax = plt.subplots()

	plt.axis('off') # no axes

	if caxis is None:
		im = plt.imshow(data, cmap=map)
	else:
		im = plt.imshow(data, cmap=map, vmin=caxis[0], vmax=caxis[1])
	if title is not None:
		plt.title( title )

	# equal aspect ratio
	ax.set_aspect('equal', 'box')
	plt.tight_layout()

	#add colorbar
	plt.colorbar(im, orientation='vertical')

def plot_histogram(data, bins=256, title="Attenuation Histogram", xlabel="Attenuation Value", ylabel="Frequency", xlim=None, ylim=None):
    """
    Creates and displays a frequency-attenuation plot (histogram) for a given scan.
    
    Parameters:
    - data: 2D numpy array containing attenuation values.
    - bins: Number of histogram bins (default is 256).
    - title: Title of the graph.
    - xlabel: Label for the x-axis.
    - ylabel: Label for the y-axis.
    - xlim: Tuple containing (min, max) for x-axis bounds.
    - ylim: Tuple containing (min, max) for y-axis bounds.
    """
    # Flatten the 2D array to 1D so matplotlib can properly bin all values
    flattened_data = np.ravel(data)
    
    # Plot the histogram
    plt.hist(flattened_data, bins=bins, color='gray', edgecolor='black', alpha=0.7)
    
    if title is not None:
        plt.title(title)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if xlim is not None:
        plt.xlim(xlim[0], xlim[1])
    if ylim is not None:
        plt.ylim(ylim[0], ylim[1])
        
    plt.show()

def save_histogram(data, storage_directory, file_name, bins=256, title="Attenuation Histogram", xlabel="Attenuation Value", ylabel="Frequency", xlim=None, ylim=None):
    """
    Creates and saves a frequency-attenuation plot (histogram) for a given scan.
    """
    full_path = get_full_path(storage_directory, file_name)
    
    # Flatten the 2D array to 1D
    flattened_data = np.ravel(data)
    
    # Plot the histogram
    plt.hist(flattened_data, bins=bins, color='gray', edgecolor='black', alpha=0.7)
    
    if title is not None:
        plt.title(title)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if xlim is not None:
        plt.xlim(xlim[0], xlim[1])
    if ylim is not None:
        plt.ylim(ylim[0], ylim[1])
        
    plt.savefig(full_path)
    plt.close()