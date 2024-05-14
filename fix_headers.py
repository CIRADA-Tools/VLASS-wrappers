import sys
from astropy.io import fits
from astropy.coordinates import SkyCoord
import os
import glob

# Check if the correct number of arguments is provided
if len(sys.argv) < 2:
    print("Usage: python fix_headers.py <pipeline(1 or 3)>")
    sys.exit(1)  # Exit the script if no arguments are provided

# Load the FITS file from the first argument
pipeline = sys.argv[1]

def update_fun(fits_file):	
	hdu_list = fits.open(fits_file, mode='update')  # Open in update mode to overwrite
	header = hdu_list[0].header  # Assuming the header to modify is in the primary HDU
	# print('RA of '+fits_file+str(header['CRVAL1']))
	if header['CRVAL1']<0:
		delta_ra = 360
		header['CRVAL1'] += delta_ra
		print('updated header of '+fits_file)
		hdu_list.flush()  # This saves the updated header to the file
		hdu_list.close()


if pipeline=='1':
	wd=os.getenv('PIPE1') + '/data/tiles/'
	fits_files=glob.glob(wd+'T*/*.fits')
	print('Checking the headers for negative RA')
	for i in fits_files:
		update_fun(i)

if pipeline=='3':
	wd=os.getenv('PIPE3_1') + '/data_out/VLASS/'
	fits_files=glob.glob(wd+'*.fits')
	print('Checking the headers for negative RA')
	for i in fits_files:
		update_fun(i)
