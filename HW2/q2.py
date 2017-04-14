import cv2
import numpy as np
import math
from matplotlib import pyplot as plt


def highlightLanes(image):

	result = (255.0)*((image/(255.0))**2)
	result = np.array(result,dtype=np.uint8)

	return result

# def grey(image):
# 	result = np.zeros(image.shape,np.uint8)

# 	rows = image.shape[0]
# 	cols = image.shape[1]

# 	for y in range(rows):
# 		for x in range(cols):
# 			r =	image[y,x,0]
# 			g = image[y,x,1]
# 			b = image[y,x,2]
# 			avg = (int(r)+int(g)+int(b))/3
# 			if (abs(r-avg) < 10) and (abs(r-avg)<10) and (abs(g-avg)<10) and (avg>65):
# 				pass
# 			else:
# 				result[y,x] = image[y,x]
			

# 	return result

# def detectLanes(image):

# 	highlighted = highlightLanes(image)
# 	canny = cv2.Canny(highlighted, 60, 160)
# 	lines = cv2.HoughLinesP(canny,1,np.pi/180,120,minLineLength=90,maxLineGap=17)
# 	leftlines = []
# 	rightline = []
# 	left = 0
# 	right = 0
# 	slope_left = 0
# 	slope_right = 0
# 	for line in lines:
# 		x1,y1,x2,y2 = line[0]
# 		# if abs(x2-x1) < 5: #almost vertical
# 		# 	continue
# 		if abs(y2-y1) < 5: #almost horizontal
# 			continue
# 		slope = float(y2-y1)/(x2-x1)

# 		if (slope < 0) and (left < 4) and abs(slope-slope_left) > 0.5: #left lane
# 			left +=1
# 			leftlines.append([x1,y1,x2,y2])
# 			slope_left = slope
# 			intercept_left = ((y1 - (slope_left * x1)) + (y2 - (slope_left * x2)))/2
# 			cv2.line(image,(x1,y1),(x2,y2),(0,0,255),4)

# 		if (slope > 0) and (right < 2) and abs(slope-slope_right) > 0.5: #right lane
# 			right = 1
# 			rightline = [x1,y1,x2,y2]
# 			slope_right = slope
# 			intercept_right = ((y1 - (slope_right * x1)) + (y2 - (slope_right * x2)))/2
# 			cv2.line(image,(x1,y1),(x2,y2),(0,0,255),4)

# 	# miny = min(leftline[1],leftline[3],rightline[1],rightline[3])
# 	# maxy = max(leftline[1],leftline[3],rightline[1],rightline[3])
	
# 	# x1 = int((miny - intercept_left)/slope_left)
# 	# x2 = int((maxy - intercept_left)/slope_left)
# 	# cv2.line(image,(x1,miny),(x2,maxy),(0,0,255),4)

# 	# x1 = int((miny - intercept_right)/slope_right)
# 	# x2 = int((maxy - intercept_right)/slope_right)
# 	# cv2.line(image,(x1,miny),(x2,maxy),(0,0,255),4)

# 	return image;	

def detectLanes(image):

	highlighted = highlightLanes(image)
	canny = cv2.Canny(highlighted, 60, 160)
	lines = cv2.HoughLinesP(canny,2,np.pi/180,180,minLineLength=120,maxLineGap=17)
	
	left = 0
	right = 0
	thetas = [0]

	for line in lines:
		x1,y1,x2,y2 = line[0]

		slope = float(y2-y1)/(x2-x1)
		theta = math.atan(slope)

		if abs(theta) < 0.1745:
			continue

		for t in thetas:
			if abs(theta-t) < 0.13:
				break
		else:
			thetas.append(theta)

			if (slope > 0) and (right < 2):
				right += 1
				cv2.line(image,(x1,y1),(x2,y2),(0,0,255),4)

			if (slope < 0) and (left < 3):
				left += 1
				cv2.line(image,(x1,y1),(x2,y2),(0,0,255),4)


	return image;	

im1 = cv2.imread('road1.png',1);
im2 = cv2.imread('road2.png',1);

#========= PART A ==========

lanes1 = detectLanes(im1);

cv2.imshow("Lane Image 1",lanes1 );
cv2.waitKey(0)
cv2.imwrite("lanes1.jpg",lanes1);

# Second image

lanes2 = detectLanes(im2);

cv2.imshow("Lane Image 2",lanes2 );
cv2.waitKey(0)
cv2.imwrite("lanes2.jpg",lanes2);				