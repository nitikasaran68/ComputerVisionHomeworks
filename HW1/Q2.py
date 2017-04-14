import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from numpy.linalg import inv

# Homogenous world coordinates of the 8 corners of the cube stored in an 8 x 3 matrix
cube_coords = np.array( [[0, 0, 0, 1],
						 [1, 0, 0, 1], 
						 [1, 1, 0, 1], 
					 	 [0, 1, 0, 1], 
						 [1, 0, 1, 1], 
						 [0, 0, 1, 1], 
						 [0, 1, 1, 1], 
						 [1, 1, 1, 1]] )


# Transformation from world frame (W) to car frame (V) 
# P_v = vTw * P_w
# where P_v and P_w are homogenous 4-vectors containing 3D coordinates along with a 4th element 1.

# This is the tranform matrix to apply translation: P_v = P_w + W_v (before rotation)
# Here W_v = (-6,8,-1) which are the coordinates of the W frame origin in V frame.
# This is the reverse of V_w = (6,-8,1)
vTw_trans = np.matrix([ [1, 0, 0, -6], 
						[0, 1, 0, 8], 
						[0, 0, 1, -1], 
						[0, 0, 0, 1]])

# Rotation of +30 degrees about the Z axis can be applied through this transorm matrix.
c = math.cos(math.radians(30))
s = math.sin(math.radians(30))
vTw_rot = np.matrix([	[c, s, 0, 0], 
						[-s, c, 0, 0], 
						[0, 0, 1, 0], 
						[0, 0, 0, 1]])

# As in this case, we apply translation first and then rotation (because translational coordinates are in original frame)
# We multiply in the following order
vTw = vTw_rot * vTw_trans;

print "Transformation from world frame (W) to car frame (V):"
print vTw

# Transformation from car frame (V) to mount frame (M)  
# P_m = mTv * P_v
# where P_m and P_v are homogenous 4-vectors containing 3D coordinates along with a 4th element 1.

# This is the tranform matrix to apply translation: P_v = P_w + W_v (before rotation)
# Here W_v = (-6,8,1) which are the coordinates of the W frame origin in V frame.
# This is the reverse of V_w = (6,-8,1)
mTv_trans = np.matrix([	[1, 0, 0, 0], 
						[0, 1, 0, 0], 
						[0, 0, 1, -4], 
						[0, 0, 0, 1]])

# Rotation of -30 degrees about the X axis can be applied through this transorm matrix.
c = math.cos(math.radians(-30))
s = math.sin(math.radians(-30))
mTv_rot = np.matrix([	[1, 0, 0, 0], 
						[0, c, s, 0], 
						[0, -s, c, 0], 
						[0, 0, 0, 1]])

# As in this case, we apply translation first and then rotation (because translational coordinates are in original frame)
# We multiply in the following order
mTv = mTv_rot * mTv_trans;

print "Transformation from car frame (V) to mount frame (M):"
print mTv

# Transformation from mount frame (M) to camera frame (C)
# P_c = cTm * P_m
# where P_m and P_c are homogenous 4-vectors containing 3D coordinates along with a 4th element 1.
# In this case, we have only translation and no rotation.
# Translation calculated in similar way as above.
cTm = np.matrix([	[1, 0, 0, 0], 
					[0, 1, 0, 2], 
					[0, 0, 1, 0], 
					[0, 0, 0, 1]])

print "Transformation from mount frame (M) to camera frame (C):"
print cTm

# We combine all these tranformations as
# P_w --> P_v --> P_m --> P_c
# P_c = cTm * (P_m)
# P_c = cTm * (mTv * P_v)
# P_c = cTm * (mTv * (vTw * P_w))
# P_c = cTm * mTv * vTw * P_w
# P_c = cTw * P_w
# cTw = cTm * mTv * vTw

cTw = cTm * mTv * vTw;
wTc = inv(cTw)

print "Transformation from world frame (W) to camera frame (C):"
print cTw

# Using inverse tranformation from camera to world to draw camera position in world
cop = np.matrix([[0], [0], [0], [1]]) #homogenous coordinates of the COP in camera frame
cop_W = np.array(wTc * cop);		  #homogenous coordinates of the COP in world frame
cop_W = cop_W.reshape((1,4))

print 'Homogenous coordinates of the COP in world frame:'
print cop_W

# 4 x 8 matrix where each column represents homogenous position vector of a cube corner in world frame
P_w = np.matrix(np.transpose(cube_coords))

# Multpilying cTw with all cube coordinates p_w to get p_c, cube corners in camera frame.
# In 4 x 8 product matrix, each column represents homogenous position vector of a cube corner in camera frame
P_c = cTw * P_w

# Camera intrinsics from Q1
fx =  3.8584530251284455e+03
fy =  3.8584530251284455e+03
cx =  1.1835000000000000e+03
cy =  2.1035000000000000e+03

# Normalized image coordinates
print "Normalized image coordinates for all cube corners:"
for i in range(8):
	p = P_c[:,i]
	n_x = p[0]/p[2]
	n_y = p[0]/p[2]
	print np.squeeze(P_w[:,i]), " --> ", n_x,n_y

# Pixel coordinates for each cube corner
# Each point is projected according to perspective projection fx * X/Z + cx, fy * Y/Z + cy
print "2D pixel coordinates in image for all cube corners:"

img_x = []
img_y = []
for i in range(8):
	p = P_c[:,i]
	img_x.append(((fx * p[0])/p[2]) + cx)
	img_y.append(((fx * p[0])/p[2]) + cx)
	print np.squeeze(P_w[:,i]), " --> ", img_x[i],img_y[i]

# Using inverse tranformation from camera to world to draw camera axes in world
X_c = np.matrix([[1],[0],[0],[1]]) # (1,0,0) position vector is along the X axis
Y_c = np.matrix([[0],[3],[0],[1]]) # (0,3,0) position vector is along the Y axis
Z_c = np.matrix([[0],[0],[1],[1]]) # (0,0,1) position vector is along the Z axis

# We will transform these points to the camera frame, and then connect them to the camera origin, to get 3 ilnes- the 3 axes. 

X_w = wTc * X_c
Y_w = wTc * Y_c
Z_w = wTc * Z_c

X_w = X_w.reshape((1,4))[0,:3].tolist()[0]
Y_w = Y_w.reshape((1,4))[0,:3].tolist()[0]
Z_w = Z_w.reshape((1,4))[0,:3].tolist()[0]

print X_w
print Y_w
print Z_w

# For each column (each 3D cube point), compute 2D image point 
# Adding COP to points to plot.
cube_coords = np.vstack((cube_coords,cop_W))

cop_W = cop_W[0,:3].tolist()

# Plotting 3D scene
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
r = [0,1]
X, Y = np.meshgrid(r, r)
ax.plot_surface(X,Y,1, alpha=0.5)
ax.plot_surface(X,Y,0, alpha=0.5)
ax.plot_surface(X,0,Y, alpha=0.5)
ax.plot_surface(X,1,Y, alpha=0.5)
ax.plot_surface(1,X,Y, alpha=0.5)
ax.plot_surface(0,X,Y, alpha=0.5)
ax.scatter3D(cube_coords[:, 0], cube_coords[:, 1], cube_coords[:, 2])
ax.plot(*zip(cop_W,X_w),color = 'r', marker = '^', label = 'X axis of camera')
ax.plot(*zip(cop_W,Y_w),color = 'g', marker = '^', label = 'Y axis of camera')
ax.plot(*zip(cop_W,Z_w),color = 'b', marker = '^', label = 'Z axis of camera')
ax.legend()
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis') 
ax.set_zlabel('Z axis') 
plt.savefig("Q2-plot")
plt.show()
# plt.clf()
# plt.plot(img_x,img_y,"ro")
# plt.title("2D scene")
# plt.xlabel("X axis")
# plt.ylabel("Y axis")
# plt.axis([-1500,1500,-1500,1500])
# plt.show()


