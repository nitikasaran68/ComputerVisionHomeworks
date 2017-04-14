import cv2
import numpy as np
# from matplotlib import pyplot as plt

drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1
prev_image = cv2.imread('AmazonGO.jpg',1)
prev_rec = []


# mouse callback function
def draw_circle(event,x,y,flags,param):
	global ix,iy,drawing,mode,img,prev_rec

	if event == cv2.EVENT_LBUTTONDOWN:
		drawing = True
		if len(prev_rec) > 0:
			minx,miny,maxx,maxy = prev_rec
			img[miny:maxy,minx:maxx] = prev_image[miny:maxy,minx:maxx]
		ix,iy = x,y

	elif event == cv2.EVENT_MOUSEMOVE:
		if drawing == True:
			minx = max(min(ix,x) - 10,0)
			maxx = min(max(ix,x) + 10,prev_image.shape[1])
			miny = max(min(iy,y) - 10,0)
			maxy = min(max(iy,y) + 10,prev_image.shape[0])
			img[miny:maxy,minx:maxx] = prev_image[miny:maxy,minx:maxx]
			cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),3)

	elif event == cv2.EVENT_LBUTTONUP:
		drawing = False
		minx = max(min(ix,x) - 5,0)
		maxx = min(max(ix,x) + 5,prev_image.shape[1])
		miny = max(min(iy,y) - 5,0)
		maxy = min(max(iy,y) + 5,prev_image.shape[0])
		prev_rec = [minx,miny,maxx,maxy]
		img[miny:maxy,minx:maxx] = prev_image[miny:maxy,minx:maxx]
		cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),3)
		# color = ['b','g','r']
		# for i,col in enumerate(color):
		# 	histr = cv2.calcHist([segmented_img[miny:maxy,minx:maxx]],[i],None,[256],[0,256])
		# 	plt.plot(histr,color = col)
		# 	plt.xlim([0,256])
		# plt.show()
		print miny, maxy, minx, maxx
		part = segmented_img[miny:maxy,minx:maxx]
		cv2.imshow('segmented',part)
		cv2.waitKey(1500)
		cv2.destroyWindow('segmented')


segmented_img = cv2.imread("AmazonGO-fuse.jpg");
img = prev_image.copy()

print segmented_img.shape
print img.shape

cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

while(1):
	cv2.imshow('image',img)
	if (cv2.waitKey(1) & 0xFF) == 27:
		break

cv2.destroyAllWindows()


