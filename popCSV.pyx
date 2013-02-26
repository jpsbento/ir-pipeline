cimport numpy as np
import jpb, pdb, os, fitsio, pyfits
import tools

@profile
cdef int popCSV(keys,operations,colheads,path,outfile):
    with open(outfile,'w') as f:
        # write out the column headers to the file.

        f.write(",".join(colheads))
        # The fits header keywords stored to retrieve values from files

        # Use the walk command to step through all of the files in all directories starting at the "root" defined above
        for root, dirs, files in os.walk(path):
            print 'Surveying directory ',root
            pb=jpb.progressbarClass(np.size(files)-1)
	    cdef int j
            j=0
            for name in files:
                if "fits.gz" in name:
                    pathAndName = os.path.join(root,name)
                    try: 
		    	 prihdr = pyfits.read_header(pathAndName) # get the primary header and values
                    	 np.ndarray[np.float64_t, ndim=2] image = pyfits.read(pathAndName) # get the image data to be analysed
		    except Exception:
		    	 prihdr = fitsio.read_header(pathAndName) # get the primary header and values
                    	 np.ndarray[np.float64_t, ndim=2] image = fitsio.read(pathAndName) # get the image data to be analysed
                    values = [root, name] # The first two entries for the row
                    #extract values from header in keys
                    for i in keys:
                        try:
                            values.append(str(prihdr[i]))

                        except Exception:
                            values.append("")

                    #start with manual operations
                    if prihdr["SAMPMODE"] == 2:
                        values.append("1")
                    else:
                        values.append(str(prihdr["MULTISAM"]))

                    # filtered version of the file used for peak and saturated
                    #filtered = tools.filter_image(pathAndName)
                    np.ndarray[np.float64_t, ndim=2] filtered = tools.filter_image(image)
                    # peak pixel
		    np.ndarray[np.float64_t] peakpix = tools.peak_coords(filtered)
                    values.append(str(peakpix[0])) # X coord of peak pixel
                    values.append(str(peakpix[1])) # Y coord of peak pixel
                    values.append(str(peakpix[2])) # value of peak pixel
                    # median pixel value in the image
                    values.append(str(np.median(image)))
                    # saturated
		    cdef int threshold
                    threshold = 20000 # max pixel value before considered saturated
                    #takes a numpy array, divides by the number of coadds and compares against threshold. returns true if peak pixel is above threshold
	       	    saturated= np.max(image/coadds) > threshold
	       	
                    values.append(str(saturated))

                    line = "\n" + ",".join(values)
                    f.write(line)
                j+=1
                pb.progress(j)
	return 1

