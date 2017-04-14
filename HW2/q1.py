import cv2
import numpy as np
import math
from matplotlib import pyplot as plt

def convolve(image,kernel):

	if kernel.shape[0] != kernel.shape[1]:
		raise 'Convolution function takes only square kernels'

	result = np.zeros(image.shape,np.uint8)

	rows = image.shape[0]
	cols = image.shape[1]

	k = kernel.shape[0];
	c = k/2

	if len(image.shape) > 2:

		colors = image.shape[2]

		for color in range(colors):
			for i in range(rows):
				for j in range(cols):
					temp = 0
					for u in range(k):
						for v in range(k):
							if (i-u+c >= 0) and (i-u+c < rows) and (j-v+c >= 0) and (j-v+c < cols):
								temp += kernel[u,v] * image[i-u+c,j-v+c,color];
					result[i,j,color] = int(temp)

	else:

		for i in range(rows):
				for j in range(cols):
					temp = 0
					for u in range(k):
						for v in range(k):
							if (i-u+c >= 0) and (i-u+c < rows) and (j-v+c >= 0) and (j-v+c < cols):
								temp += kernel[u,v] * image[i-u+c,j-v+c];
					result[i,j] = int(temp)

			
	return result


def sobel(image,k,thresh):

	image = np.array(image,dtype = np.float32)
	result = np.zeros(image.shape,dtype = np.uint8)
	resultx = np.zeros(image.shape,dtype = np.uint8)
	resulty = np.zeros(image.shape,dtype = np.uint8)

	sobely = cv2.getDerivKernels(1, 0, k)
	sobely = np.outer(sobely[0], sobely[1])
	sobely = sobely/np.sum(sobely[:1,:])

	sobelx = cv2.getDerivKernels(0, 1, k)
	sobelx = np.outer(sobelx[0], sobelx[1])
	sobelx = sobely/np.sum(sobelx[:,:1])

	rows = image.shape[0]
	cols = image.shape[1]

	c = k/2

	for i in range(c,rows-c):
		for j in range(c,cols-c):
			Gx = 0
			Gy = 0
			for u in range(k):
				for v in range(k):
					Gx += sobelx[u,v] * image[i+u-c,j+v-c]
					Gy += sobely[u,v] * image[i+u-c,j+v-c]

			resultx[i,j] = int(abs(Gx))
			resulty[i,j] = int(abs(Gy))

			temp = int(math.sqrt((Gx**2)+(Gy**2)))

			if temp > thresh:
				result[i,j] = temp
			
	return [result,resultx,resulty]

def gaussian(k,sigma):

	c = k/2;
	kernel = np.zeros((k,k));
	pi = 3.141592; 
	summ = 0
	sigma2 = math.pow(sigma,2);

	for i in range(k):
		for j in range(k):
			temp = -(math.pow(i-c,2) + math.pow(j-c,2)) / (2 * sigma2)
			temp = math.exp(temp);
			kernel[i,j]  = temp #/ (2 * pi * sigma2);
			summ += kernel[i,j]

	kernel = kernel/summ
	return kernel;


im1 = cv2.imread('road1.png',1);
im2 = cv2.imread('road2.png',1);
im1_gray = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
im2_gray = cv2.cvtColor(im2,cv2.COLOR_BGR2GRAY)


#===================================================== PART A ==================================================================

# road1.png

# sigma = 1
kernel1 = gaussian(11,1)
blurred1_1 = convolve(im1,kernel1)
cv2.imwrite('road1-blurred1.png',blurred1_1)

# sigma = 3
kernel3 = gaussian(11,3)
blurred1_3 = convolve(im1,kernel3)
cv2.imwrite('road1-blurred3.png',blurred1_3)

# sigma = 7
kernel7 = gaussian(11,7)
blurred1_7 = convolve(im1,kernel7)
cv2.imwrite('road1-blurred7.png',blurred1_7)

# show and write results
plt.subplot(131),
plt.imshow(blurred1_1),plt.title('Sigma = 1')
plt.xticks([]), plt.yticks([])
plt.subplot(132),
plt.imshow(blurred1_3),plt.title('Sigma = 3')
plt.xticks([]), plt.yticks([])
plt.subplot(133),
plt.imshow(blurred1_7),plt.title('Sigma = 7')
plt.xticks([]), plt.yticks([])
plt.savefig("q1a-road1.png")
plt.show()

# road2.png

# sigma = 1
blurred2_1 = convolve(im2,kernel1)
cv2.imwrite('road2-blurred1.png',blurred2_1)

# sigma = 3
blurred2_3 = convolve(im2,kernel3)
cv2.imwrite('road2-blurred3.png',blurred2_3)

# sigma = 7
blurred2_7 = convolve(im2,kernel7)
cv2.imwrite('road2-blurred7.png',blurred2_7)

show and write results
plt.subplot(131),
plt.imshow(blurred2_1),plt.title('Sigma = 1')
plt.xticks([]), plt.yticks([])
plt.subplot(132),
plt.imshow(blurred2_3),plt.title('Sigma = 3')
plt.xticks([]), plt.yticks([])
plt.subplot(133),
plt.imshow(blurred2_7),plt.title('Sigma = 7')
plt.xticks([]), plt.yticks([])
plt.savefig("q1a-road2.png")
plt.show()


# ===================================================== PART B ==================================================================

# road1.png

edge,edgex,edgey = sobel(im1_gray,3,0)

cv2.imwrite('road1-edgex-3.png',edgex)
cv2.imwrite('road1-edgey-3.png',edgey)
cv2.imwrite('road1-edge-3.png',edge)

plt.clf()
plt.subplot(131),
plt.imshow(edgex,cmap='gray'),plt.title('X Gradient')
plt.xticks([]), plt.yticks([])
plt.subplot(132),
plt.imshow(edgey,cmap='gray'),plt.title('Y Gradient')
plt.xticks([]), plt.yticks([])
plt.subplot(133),
plt.imshow(edge,cmap='gray'),plt.title('Edges')
plt.xticks([]), plt.yticks([])
plt.show()


edge,edgex,edgey = sobel(im1_gray,7,10)

cv2.imwrite('road1-edgex-7.png',edgex)
cv2.imwrite('road1-edgey-7.png',edgey)
cv2.imwrite('road1-edge-7.png',edge)

plt.clf()
plt.subplot(131),
plt.imshow(edgex,cmap='gray'),plt.title('X Gradient')
plt.xticks([]), plt.yticks([])
plt.subplot(132),
plt.imshow(edgey,cmap='gray'),plt.title('Y Gradient')
plt.xticks([]), plt.yticks([])
plt.subplot(133),
plt.imshow(edge,cmap='gray'),plt.title('Edges')
plt.xticks([]), plt.yticks([])
plt.show()

edge,edgex,edgey = sobel(im1_gray,11,20)

cv2.imwrite('road1-edgex-11.png',edgex)
cv2.imwrite('road1-edgey-11.png',edgey)
cv2.imwrite('road1-edge-11.png',edge)

plt.clf()
plt.subplot(131),
plt.imshow(edgex,cmap='gray'),plt.title('X Gradient')
plt.xticks([]), plt.yticks([])
plt.subplot(132),
plt.imshow(edgey,cmap='gray'),plt.title('Y Gradient')
plt.xticks([]), plt.yticks([])
plt.subplot(133),
plt.imshow(edge,cmap='gray'),plt.title('Edges')
plt.xticks([]), plt.yticks([])
plt.show()

road2.png

edge,edgex,edgey = sobel(im2_gray,3,5)

cv2.imwrite('road2-edgex-3.png',edgex)
cv2.imwrite('road2-edgey-3.png',edgey)
cv2.imwrite('road2-edge-3.png',edge)

plt.clf()
plt.subplot(131),
plt.imshow(edgex,cmap='gray'),plt.title('x Gradient')
plt.xticks([]), plt.yticks([])
plt.subplot(132),
plt.imshow(edgey,cmap='gray'),plt.title('y Gradient')
plt.xticks([]), plt.yticks([])
plt.subplot(133),
plt.imshow(edge,cmap='gray'),plt.title('Edges')
plt.xticks([]), plt.yticks([])
plt.show()


edge,edgex,edgey = sobel(im2_gray,7,10)

cv2.imwrite('road2-edgex-7.png',edgex)
cv2.imwrite('road2-edgey-7.png',edgey)
cv2.imwrite('road2-edge-7.png',edge)

plt.clf()
plt.subplot(131),
plt.imshow(edgex,cmap='gray'),plt.title('X Gradient')
plt.xticks([]), plt.yticks([])
plt.subplot(132),
plt.imshow(edgey,cmap='gray'),plt.title('Y Gradient')
plt.xticks([]), plt.yticks([])
plt.subplot(133),
plt.imshow(edge,cmap='gray'),plt.title('Edges')
plt.xticks([]), plt.yticks([])
plt.show()

edge,edgex,edgey = sobel(im2_gray,11,20)

cv2.imwrite('road2-edgex-11.png',edgex)
cv2.imwrite('road2-edgey-11.png',edgey)
cv2.imwrite('road2-edge-11.png',edge)

plt.clf()
plt.subplot(131),
plt.imshow(edgex,cmap='gray'),plt.title('X Gradient')
plt.xticks([]), plt.yticks([])
plt.subplot(132),
plt.imshow(edgey,cmap='gray'),plt.title('Y Gradient')
plt.xticks([]), plt.yticks([])
plt.subplot(133),
plt.imshow(edge,cmap='gray'),plt.title('Edges')
plt.xticks([]), plt.yticks([])
plt.show()

# ===================================================== PART C ==================================================================

# road1.png

blurred1_7 = cv2.imread("road1-blurred7.png",0)
sharpened1 = (1.6*im1_gray) -(0.4*blurred1_7)

cv2.imwrite('sharpened1.png',sharpened1)

# compare with original
plt.subplot(121),plt.imshow(im1_gray,cmap='gray'),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(sharpened1,cmap='gray'),plt.title('Sharpened')
plt.xticks([]), plt.yticks([])
plt.savefig("q1c-road1.png")
plt.show()

# road2.png

blurred2_7 = cv2.imread("road2-blurred7.png",0)
sharpened2 = (1.6*im2_gray) - (0.4*blurred2_7)

cv2.imwrite('sharpened2.png',sharpened2)

plt.subplot(121),plt.imshow(im2_gray,cmap='gray'),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(sharpened2,cmap='gray'),plt.title('Sharpened')
plt.xticks([]), plt.yticks([])
plt.savefig("q1c-road2.png")
plt.show()

				