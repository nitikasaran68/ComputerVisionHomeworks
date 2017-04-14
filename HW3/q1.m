run('/Users/nitikasaran/Desktop/CSE344-CV/vlfeat-0.9.20/toolbox/vl_setup')

%%
vehsub = {'GTI_Far', 'GTI_Left', 'GTI_MiddleClose', 'GTI_Right', 'KITTI_extracted'};
nonvehsub = {'Extras', 'GTI'};
vehpath =  {'vehicle'};
nonvehpath = {'non-vehicle'};
trainhist = [];
testhist = [];

%%
temp = vehsub;
vpath = fullfile('vehicles', temp);
vehdata = imageDatastore(vpath, 'LabelSource', 'foldernames');
[vehtrain, vehtest] = splitEachLabel(vehdata, 0.8, 'randomize');
vehtrain_len = length(vehtrain.Files);
vehtest_len = length(vehtest.Files);
temp = nonvehsub;
nvpath = fullfile('non-vehicles', temp);
nonvehdata = imageDatastore(nvpath, 'LabelSource', 'foldernames');
[nonvehtrain, nonvehtest] = splitEachLabel(nonvehdata, 0.8, 'randomize');
nonvehtrain_len = length(nonvehtrain.Files);
nonvehtest_len = length(nonvehtest.Files);


%%

train_data_paths = cell(vehtrain_len +nonvehtrain_len , 1);
trainpathlen = length(train_data_paths);

train_data_paths(1:vehtrain_len) = vehtrain.Files;
train_data_paths(1+vehtrain_len:trainpathlen) = nonvehtrain.Files;
train_data_labels = cell(length(train_data_paths), 1);
train_data_labels(1:vehtrain_len) = {'vehicle'};
train_data_labels(1+vehtrain_len:trainpathlen) = {'non-vehicle'};

%%
test_data_paths = cell(vehtest_len + nonvehtest_len, 1);
testpathlen = length(test_data_paths);
test_data_paths(1:vehtest_len) = vehtest.Files;
test_data_paths(1+vehtest_len:testpathlen) = nonvehtest.Files;
test_data_labels = cell(length(test_data_paths), 1);
test_data_labels(1:vehtest_len) = vehpath;
test_data_labels(1+vehtest_len:length(test_data_paths)) = nonvehpath;

%
feats = [];
for i = 1: trainpathlen
    img = imread(train_data_paths{i});
    img = single(rgb2gray(img)) ;
    [f,d] = vl_sift(img);
    feats = [feats d];
end

%%
% features = load('/Users/nitikasaran/Documents/MATLAB/features.mat');

%%
[centers, assgt] = vl_kmeans(double(feats ), 20, 'distance', 'l1', 'algorithm', 'elkan','MaxNumIterations', 150);
% assgt = load('/Users/nitikasaran/Documents/MATLAB/cpt.mat');
kdt = vl_kdtreebuild(assgt);


%%
for i = 1:trainpathlen
    im = imread(train_data_paths{i});
    im = single(rgb2gray(im));
    [~, d] = vl_sift(im);
    [index , ~] = vl_kdtreequery(kdt, assgt, double(d));
    ind = double(index);
    his = hist(ind, 20);
    trainhist(i, :) = his;
    i
end
%%
for i = 1:testpathlen
    im = imread(test_data_paths{i});
    im = single(rgb2gray(im));
    [~, d] = vl_sift(im);
    [index , ~] = vl_kdtreequery(kdt, assgt, double(d));
    his = hist(double(index), 20);
    testhist(i, :) = his;
    i
end

%% C
knnmod = fitcknn(trainhist,train_data_labels,'NumNeighbors',5,'Standardize',1);
myans = predict(knnmod,testhist);
[C,order]=confusionmat(test_data_labels,myans);
st = strcmp(test_data_labels,  myans);
accuracy = sum(st) / numel(test_data_labels);
disp(accuracy);



