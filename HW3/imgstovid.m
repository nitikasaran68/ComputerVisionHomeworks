workingDir = '/Users/nitikasaran/Downloads/tracking_video_dataset/3';
imageNames = dir(fullfile(workingDir,'img','*.jpg'));
imageNames = {imageNames.name}';
outputVideo = VideoWriter(fullfile(workingDir,'../3'));
outputVideo.FrameRate = 15;
open(outputVideo)
for ii = 1:length(imageNames)
   img = imread(fullfile(workingDir,'img',imageNames{ii}));
   writeVideo(outputVideo,img)
end
close(outputVideo)
videoFileReader = vision.VideoFileReader('/Users/nitikasaran/Downloads/tracking_video_dataset/3.avi');
videoFrame      = step(videoFileReader);