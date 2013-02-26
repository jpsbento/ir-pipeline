#!/usr/bin/python

import os
import fitsio
import tools # from tools.py
import jpb, time
import pdb
import numpy as np

print 'Program started at time:'
print time.asctime( time.localtime(time.time()) )

path = jpb.ask('Which directory to run this code?','./') # path to root of directory to walk through, relative to location of script
outfile = path + "testMedian.csv" # the output file to write to

keys = ["FILTER", \
        "EFFWAVE", \
        "OBJECT", \
        "TARGNAME", \
        "CAMNAME", \
        "IMAGETYP", \
        "COADDS", \
        "ITIME", \
        "DATE-OBS", \
        "MJD-OBS", \
        "UTC", \
        "EL", \
        "RA", \
        "DEC", \
        "NAXIS1", \
        "NAXIS2", \
        "PIXSCALE", \
        "SLITNAME" \
        ]

# The headers for analysis done on the files
# MULTISAM is 1 if SAMPMODE is 2, else write value in header
# PEAKPIX is one operation, but returns 2 values, needs two columns
# SATURATED be sure to set the threshold value for level before saturated
operations = ["MULTISAM", \
              "PEAKPIX(X)", \
              "PEAKPIX(Y)", \
              "PEAK_VALUE", \
              "MEDIAN_VALUE", \
              "SATURATED" \
             ]

# try to be fancy writing the column headers
# Directory and Filename are always going to be the first two columns for the output
colheads = ["DIRECTORY", \
            "FILENAME" \
           ]

colheads=colheads+keys+operations

########################
# Begin main part of the script
########################

with open(outfile,'w') as f:
    # write out the column headers to the file.

    f.write(",".join(colheads))
    # The fits header keywords stored to retrieve values from files


    # Use the walk command to step through all of the files in all directories starting at the "root" defined above
    for root, dirs, files in os.walk(path):
        print 'Surveying directory ',root
        pb=jpb.progressbarClass(np.size(files)-1)
        j=0
        for name in files:
            if "fits.gz" in name:
                pathAndName = os.path.join(root,name)
                prihdr = fitsio.read_header(pathAndName) # get the primary header and values
                image = fitsio.read(pathAndName) # get the image data to be analysed
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
                filtered = tools.filter_image(image)
                # peak pixel
                peakpix = tools.peak_coords(filtered)
                values.append(str(peakpix[0])) # X coord of peak pixel
                values.append(str(peakpix[1])) # Y coord of peak pixel
                values.append(str(peakpix[2])) # value of peak pixel
                # median pixel value in the image
                values.append(str(tools.median(image)))
                # saturated
                threshold = 20000 # max pixel value before considered saturated
                saturated = tools.saturated(filtered, prihdr["coadds"], threshold)
                values.append(str(saturated))

                line = "\n" + ",".join(values)
                f.write(line)
            j+=1
            pb.progress(j)


print 'Program finished at time:'
print time.asctime( time.localtime(time.time()) )
