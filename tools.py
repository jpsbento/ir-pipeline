#e.g. 
#import matplotlib.pyplot as plt
#import median_filter
#im = median_filter.filter_image('U7N2/NIRC2_sci_8110_1/raw/N2.20011218.48401.fits.gz')
#plt.draw()
#plt.imshow(im)
#import pyfits
import numpy as np

def filter_image(image):
	#image = pyfits.getdata(infile)
	image1 = np.roll(image,1,0)
	image2 = np.roll(image,-1,0)
	cube = np.ndarray((image.shape[0],image.shape[1],9))
	cube[:,:,0] = image
	cube[:,:,1] = image1
	cube[:,:,2] = image2
	cube[:,:,3] = np.roll(image,1,1)
	cube[:,:,4] = np.roll(image1,1,1)
	cube[:,:,5] = np.roll(image2,1,1)
	cube[:,:,6] = np.roll(image,-1,1)
	cube[:,:,7] = np.roll(image1,-1,1)
	cube[:,:,8] = np.roll(image2,-1,1)
	return np.median(cube,2)

def peak_coords(image):
# takes a numpy array and returns the x,y coords of the peak value
# takes the median filtered image from filter_image() as input
    shape = np.shape(image)
    maxindex = image.argmax()
    coords = []
    coords.append(maxindex % shape[1]) # max pixel x value
    coords.append(int(maxindex/shape[1])) # max pixel y value
    coords.append(image.max())
    return coords

def saturated(image, coadds, threshold):
#takes a numpy array, divides by the number of coadds and compares against threshold
# returns true if peak pixel is above threshold
	return np.max(image/coadds) > threshold

def median(image):
#returns the median value of a numpy array
    return np.median(image)
