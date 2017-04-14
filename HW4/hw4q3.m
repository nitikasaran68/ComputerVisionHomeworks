cd '/Users/nitikasaran/Desktop/CSE344-CV/HW4'
run('/Users/nitikasaran/Desktop/CSE344-CV/vlfeat-0.9.20/toolbox/vl_setup')

im1 = imread('data/q4data/image1.jpg');
im2 = imread('data/q4data/image2.jpg') ;

% make single
im1 = im2single(im1) ;
im2 = im2single(im2) ;

% make grayscale
if size(im1,3) > 1, im1g = rgb2gray(im1) ; else, im1g = im1 ; end
if size(im2,3) > 1, im2g = rgb2gray(im2) ; else, im2g = im2 ; end

[f1,d1] = vl_sift(im1g) ;
[f2,d2] = vl_sift(im2g) ;

[matches, scores] = vl_ubcmatch(d1,d2) ;

numMatches = size(matches,2) ;

[drop, perm] = sort(scores, 'descend') ;
matches = matches(:, perm) ;
scores  = scores(perm);
% matches = matches(:,1:500);
% scores = scores(1:500);


X1 = f1(1:2,matches(1,:)) ; X1(3,:) = 1 ;
X2 = f2(1:2,matches(2,:)) ; X2(3,:) = 1 ;

%========== Homography ============

H  = cell(100,1);
score = zeros(1,100);
ok = cell(100,1);

for t = 1:100
  % estimate homography
  subset = vl_colsubset(1:numMatches, 4) ;
  A = [] ;
  for i = subset
    A = cat(1, A, kron(X1(:,i)', vl_hat(X2(:,i)))) ;
  end
  [U,S,V] = svd(A) ;
  H{t} = reshape(V(:,9),3,3) ;

  % score homography
  X2_ = H{t} * X1 ;
  du = X2_(1,:)./X2_(3,:) - X2(1,:)./X2(3,:) ;
  dv = X2_(2,:)./X2_(3,:) - X2(2,:)./X2(3,:) ;
  ok{t} = (du.*du + dv.*dv) < 36 ;
  score(t) = sum(ok{t}) ;
end

[score, best] = max(score) ;
H = H{best} ;
ok = ok{best} ;

% draw matches

dh1 = max(size(im2,1)-size(im1,1),0) ;
dh2 = max(size(im1,1)-size(im2,1),0) ;

figure(1) ; clf ;

imagesc([padarray(im1,dh1,'post') padarray(im2,dh2,'post')]) ;
o = size(im1,2) ;
line([f1(1,matches(1,:));f2(1,matches(2,:))+o], ...
     [f1(2,matches(1,:));f2(2,matches(2,:))]) ;
title('Best 500 matches') ;
axis image off ;
drawnow ;
savefig('matches.fig');

% ======= warp ==========

H = H/H(3,3);
tr = projective2d(H');
warped = imwarp(im1,tr);
imwrite(warped,'q3/im1toim2.jpg');

tr = projective2d(inv(H'));
warped = imwarp(im2,tr);
imwrite(warped,'q3/im2toim1.jpg');




