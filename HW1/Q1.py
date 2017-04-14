import os
from xml.etree.ElementTree import parse, Element
import random
import matplotlib.pyplot as plt

## ======================== PART A ===================================

# with all DOFs covered (S1)
print "Calibrating for 20 images with all DOFs covered"

# editing configuration file to set image list.
print "Editing configuration file to set image list ..."
config_file = parse("default.xml");
root = config_file.getroot()
input_file = root.find('Settings').find('Input')
input_file.text = '"imgs_all_DOF.xml"'
config_file.write('default.xml',encoding="utf-8", xml_declaration=True)
f = open('default.xml','r+')
f.write('<?xml version="1.0"?>                 \n')
f.close()

# performing calibration
print "Running calibration program ..."
os.system("./calibrate");

# extracting output
print "\n\nRESULTS:\n"
out_file = parse("out_camera_data.xml");
root = out_file.getroot()
error_tag = root.find("Avg_Reprojection_Error")
error = float(error_tag.text);
print "Average reprojection error = ",error
intrinsics_tag = root.find("Camera_Matrix").find("data")
intrinsics = intrinsics_tag.text.split(' ');
intrinsics = [x for x in intrinsics if x != '' and x!='\n']
print "Estimated intrinsics:"
print "fx = ",intrinsics[0]
print "fy = ",intrinsics[4]
print "cx = ",intrinsics[2]
print "cy = ",intrinsics[5]
distortion_tag = root.find("Distortion_Coefficients").find("data")
distortion = distortion_tag.text.split(' ');
distortion = [float(x) for x in distortion if x != '' and x!='\n']
# Distortion coefficients = (k_1  k_2  p_1  p_2  k_3)
print "Estimated distortion coefficients:", distortion


##=======================================##

# first twenty (S2)
print "Calibrating for first 20 images"

# preparing image list
print "Preparing image list ..."
my_imgs = []
lis = os.listdir("images");
for fil in lis:
	if fil.split('.')[1] == "jpg":
		my_imgs.append("images/" + fil)

imgs_text = "\n";
count = 0

for img in my_imgs:
	imgs_text += img + "\n"
	count += 1
	if count >=20:
		break;


# editing file containing image list.
print "Editing image list file ..."
imgs_file = parse("imgs.xml")
root = imgs_file.getroot()
imgs_tag = root.find("images")
imgs_tag.text = imgs_text
imgs_file.write("imgs.xml",encoding='utf-8', xml_declaration=True)
f = open('imgs.xml','r+')
f.write('<?xml version="1.0"?>                 \n')
f.close()

# editing configuration file to set image list.
print "Editing configuration file to set image list ..."
config_file = parse("default.xml");
root = config_file.getroot()
input_file = root.find('Settings').find('Input')
input_file.text = '"imgs.xml"'
config_file.write('default.xml',encoding='utf-8', xml_declaration=True)
f = open('default.xml','r+')
f.write('<?xml version="1.0"?>                 \n')
f.close()

# performing calibration
print "Running calibration program ..."
os.system("./calibrate");

# extracting output
print "\n\nRESULTS:\n"
out_file = parse("out_camera_data.xml");
root = out_file.getroot()
error_tag = root.find("Avg_Reprojection_Error")
error = float(error_tag.text);
print "Average reprojection error for first 20 images: ",error
intrinsics_tag = root.find("Camera_Matrix").find("data")
intrinsics = intrinsics_tag.text.split(' ');
intrinsics = [x for x in intrinsics if x != '' and x!='\n']
print "Estimated intrinsics:"
print "fx = ",intrinsics[0]
print "fy = ",intrinsics[4]
print "cx = ",intrinsics[2]
print "cy = ",intrinsics[5]
distortion_tag = root.find("Distortion_Coefficients").find("data")
distortion = distortion_tag.text.split(' ');
distortion = [float(x) for x in distortion if x != '' and x!='\n']
# Distortion coefficients = (k_1  k_2  p_1  p_2  k_3)
print "Estimated distortion coefficients:", distortion



## ======================== PART B ===================================

# editing configuration file to set image list.
print "Editing configuration file to set image list ..."
config_file = parse("default.xml");
root = config_file.getroot()
input_file = root.find('Settings').find('Input')
input_file.text = '"imgs.xml"'
config_file.write('default.xml',encoding='utf-8', xml_declaration=True)
f = open('default.xml','r+')
f.write('<?xml version="1.0"?>                 \n')
f.close()

plot_x = []
plot_y = []

my_imgs = []
lis = os.listdir("images");
for fil in lis:
	if fil.split('.')[1] == "jpg":
		my_imgs.append("images/" + fil)

for N in range(5,51,5):

	print "Calibrating for ",N," random images"
	
	sample = random.sample(my_imgs, N)

	# preparing image list
	print "Preparing image list using random sampling ..."

	imgs_text = "\n";

	for img in sample:
		imgs_text += img + "\n"

	# editing file containing image list.
	print "Editing image list file ..."
	imgs_file = parse("imgs.xml")
	root = imgs_file.getroot()
	imgs_tag = root.find("images")
	imgs_tag.text = imgs_text
	imgs_file.write("imgs.xml",encoding='utf-8', xml_declaration=True)
	f = open('imgs.xml','r+')
	f.write('<?xml version="1.0"?>                 \n')
	f.close()

	# performing calibration
	print "Running calibration program ..."
	os.system("./calibrate > out");

	# extracting output
	print "\n\nRESULTS:\n"
	out_file = parse("out_camera_data.xml");
	root = out_file.getroot()
	error_tag = root.find("Avg_Reprojection_Error")
	error = float(error_tag.text);
	print "Average reprojection error: ",error
	print
	print

	plot_x.append(N)
	plot_y.append(error)

# print "Plotting...helloo"

# # hard-coded due to memory issues.
# plot_x = [5,10,15,20,25,30,35,40,45,50]
# plot_y = [4.4390, 2.614, 3.4355, 3.62536, 3.1861, 3.7217, 3.8068, 3.7287, 3.5358, 3.7823]
# plt.xlabel('Number of images (N)')
# plt.ylabel('Avg reprojection error')
# plt.savefig("Q1-plot")
# plt.show()







