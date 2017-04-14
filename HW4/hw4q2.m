cd '/Users/nitikasaran/Desktop/CSE344-CV/HW4'

% ========= Floor Image ============

figure(1)
im = imread('data/floor.jpg');
% 
% %=========== Affine Rectification =============

imshow(im)
xlabel('Select a pair of parallel lines by clicking on 2 points per line. Press enter once done')
[x,y] = getpts
close Figure 1

p1 = [x(1) y(1) 1];
p2 = [x(2) y(2) 1];
p3 = [x(3) y(3) 1];
p4 = [x(4) y(4) 1];

l1 = cross(p1,p2);
l2 = cross(p3,p4);

% Get vanishing point for first pair of lines.
a = cross(l1, l2);
a = a/a(1,3);

imshow(im)
xlabel('Select another pair of parallel lines by clicking on 2 points per line. Press enter once done')
[x,y] = getpts
close Figure 1

p1 = [x(1) y(1) 1];
p2 = [x(2) y(2) 1];
p3 = [x(3) y(3) 1];
p4 = [x(4) y(4) 1];

l1 = cross(p1, p2);
l2 = cross(p3, p4);

% Get vanishing point for first pair of lines.
b = cross(l1, l2);
b = b/ b(1,3); 

% line at infinity
l = cross(a, b);
l = l/l(1,3);

% compute the transformation matrix H....
H = [1 0 0; 0 1 0; l(1, 1) l(1, 2) 1];
tr = projective2d(H');

% compute the warped image using H.
rectified = imwarp(im, tr);
imshow(rectified) % required affine rectified image...
imwrite(rectified,'q2/floor-affinerectified.jpg')
stop;

%============= Metric Rectification ===============

im = imread('q2/floor-affinerectified.jpg');
% im = rectified;
imshow(im)
xlabel('Select a pair of orthogonal lines from the image')
[x,y] = getpts;
line([x(1) x(2)],[y(1) y(2)])
line([x(3) x(4)],[y(3) y(4)])
tem = getpts;
close Figure 1

p1 = [x(1) y(1) 1];
p2 = [x(2) y(2) 1];
p3 = [x(3) y(3) 1];
p4 = [x(4) y(4) 1];

l1 = cross(p1, p2);
m1 = cross(p3, p4);

l11 = l1(1,1);
l12 = l1(1,2);
m11 = m1(1,1);
m12 = m1(1,2);

imshow(im)
xlabel('Select another pair of orthogonal lines from the image')
[x,y] = getpts;
close Figure 1

p1 = [x(1) y(1) 1];
p2 = [x(2) y(2) 1];
p3 = [x(3) y(3) 1];
p4 = [x(4) y(4) 1];

l2 = cross(p1, p2);
m2 = cross(p3, p4);

l21 = l2(1,1);
l22 = l2(1,2);
m21 = m2(1,1);
m22 = m2(1,2);

% solving for the linear constraint on 2 × 2 matrix S...

M = [l11*m11 (l11*m12 + l12*m11) ; l21*m21 (l21*m22 + l22*m21)];
b = [-l12*m12;-l22*m22 ];

x = linsolve(M,b);

S = eye(2);
S(1,1) = x(1);
S(1,2) = x(2);
S(2,1) = x(2);

% obtaining  homography
[U,D,V] = svd(S);
sqrtD = sqrt(D);
U_T = transpose(U);
A = U*sqrtD * U_T;
% A_t = transpose(A);
% AAt = A*(A_t);
H2 = eye(3);
H2(1,1) = A(1,1);
H2(1,2) = A(1,2);
H2(2,1) = A(2,1);
H2(2,2) = A(2,2);

tr = projective2d(inv(H2));
rectified = imwarp(im, tr);
imshow(rectified); % required metric rectified image...
imwrite(rectified,'q2/floor-metricrectified.jpg')

%========= Hall Image ============

figure(1)
im = imread('data/hall.jpg');
imshow(im)
xlabel('Select a pair of parallel lines by clicking on 2 points per line. Press enter once done')
[x,y] = getpts
close Figure 1

p1 = [x(1) y(1) 1];
p2 = [x(2) y(2) 1];
p3 = [x(3) y(3) 1];
p4 = [x(4) y(4) 1];

l1 = cross(p1,p2);
m1 = cross(p3,p4);

% Get vanishing point for first pair of lines.
a = cross(l1, m1);
a = a/a(1,3);

imshow(im)
xlabel('Select another pair of parallel lines by clicking on 2 points per line. Press enter once done')
[x,y] = getpts
close Figure 1

p1 = [x(1) y(1) 1];
p2 = [x(2) y(2) 1];
p3 = [x(3) y(3) 1];
p4 = [x(4) y(4) 1];

l1 = cross(p1, p2);
m1 = cross(p3, p4);

% Get vanishing point for first pair of lines.
b = cross(l1, m1);
b = b/ b(1,3); 

% line at infinity
l = cross(a, b);
l = l/l(1,3);

% compute the transformation matrix H....
H = [1 0 0; 0 1 0; l(1, 1) l(1, 2) 1];
tr = projective2d(H');

% compute the warped image using H.
rectified = imwarp(im, tr);
imshow(rectified)
imwrite(rectified,'q2/hall-affinerectified.jpg')


% ======== Metric Rectification =========

im = imread('q2/hall-affinerectified.jpg');
% im = rectified;
imshow(im)
xlabel('Select a pair of orthogonal lines from the image')
[x,y] = getpts;
line([x(1) x(2)],[y(1) y(2)])
line([x(3) x(4)],[y(3) y(4)])
tem = getpts;
close Figure 1

p1 = [x(1) y(1) 1];
p2 = [x(2) y(2) 1];
p3 = [x(3) y(3) 1];
p4 = [x(4) y(4) 1];

l1 = cross(p1, p2);
m1 = cross(p3, p4);

l11 = l1(1,1);
l12 = l1(1,2);
m11 = m1(1,1);
m12 = m1(1,2);

imshow(im)
xlabel('Select another pair of orthogonal lines from the image')
[x,y] = getpts;
close Figure 1

p1 = [x(1) y(1) 1];
p2 = [x(2) y(2) 1];
p3 = [x(3) y(3) 1];
p4 = [x(4) y(4) 1];

l2 = cross(p1, p2);
m2 = cross(p3, p4);

l21 = l2(1,1);
l22 = l2(1,2);
m21 = m2(1,1);
m22 = m2(1,2);

% solving for the linear constraint on 2 × 2 matrix S...

M = [l11*m11 (l11*m12 + l12*m11) ; l21*m21 (l21*m22 + l22*m21)];
b = [-l12*m12;-l22*m22 ];

x = linsolve(M,b);

S = eye(2);
S(1,1) = x(1);
S(1,2) = x(2);
S(2,1) = x(2);

% obtaining  homography
[U,D,V] = svd(S);
sqrtD = sqrt(D);
U_T = transpose(U);
A = U*sqrtD * U_T;
% A_t = transpose(A);
% AAt = A*(A_t);
H2 = eye(3);
H2(1,1) = A(1,1);
H2(1,2) = A(1,2);
H2(2,1) = A(2,1);
H2(2,2) = A(2,2);
% if H2(1,1) < 0
%     H2(1,1) = -H2(1,1);
% 
% elseif H2(2,2) < 0
%     H2(2,2) = -H2(2,2);
% end

tr = projective2d(inv(H2));
rectified = imwarp(im, tr);
imshow(rectified); % required metric rectified image...
imwrite(rectified,'q2/hall-metricrectified.jpg')