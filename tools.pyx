cimport numpy as np

def filter_image(np.ndarray[np.float64_t, ndim=2] image):
	cdef np.ndarray[np.float64_t, ndim=2] image1 = np.roll(image,1,0)
	cdef np.ndarray[np.float64_t, ndim=2] image2 = np.roll(image,-1,0)
	cdef np.ndarray[np.float64_t, ndim=3] cube = np.ndarray((image.shape[0],image.shape[1],9))
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

def peak_coords(np.ndarray[np.float64_t, ndim=2] image):
# takes a numpy array and returns the x,y coords of the peak value
# takes the median filtered image from filter_image() as input
    shape = np.shape(image)
    cdef int maxindex = image.argmax()
    cdef np.ndarray[nd.float64_t] coords = []
    coords.append(maxindex % shape[1]) # max pixel x value
    coords.append(int(maxindex/shape[1])) # max pixel y value
    coords.append(image.max())
    return coords

