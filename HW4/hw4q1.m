cd '/Users/nitikasaran/Desktop/CSE344-CV/HW4'
load('data/q1data.mat')
H1 = [sqrt(3) -1 1; 1 sqrt(3) 1; 0 0 2];
H2 = [1 -1 1; 1 1 0; 0 0 1];
H3 = [1 1 0; 0 2 0; 0 0 1];
H4 = [sqrt(3) -1 1; 1 sqrt(3) 1; 0.25 0.5 2];

l = length(startpoints);
clf();
hold on;
for i = 1:l
    x = [startpoints(:,i) endpoints(:,i)];
    plot(x(1,:),x(2,:))
end
hold off;

savefig('q1/origlines.fig');
clf();

startpoints1 = zeros(2,l);
for i = 1:l
    x = [startpoints(:,i); 1];
    x = H1 * x;
    startpoints1(:,i) = x(1:2)/x(3);
end

endpoints1 = zeros(2,l);
for i = 1:l
    x = [endpoints(:,i); 1];
    x = H1 * x;
    endpoints1(:,i) = x(1:2)/x(3);
end


% subplot(2,2,1)

hold on;
for i = 1:l
    x = [startpoints1(:,i) endpoints1(:,i)];
    plot(x(1,:),x(2,:))
end
hold off;

savefig('q1/h1.fig');
clf();

startpoints2 = zeros(2,l);
for i = 1:l
    x = [startpoints(:,i); 1];
    x = H2 * x;
    startpoints2(:,i) = x(1:2)/x(3);
end

endpoints2 = zeros(2,l);
for i = 1:l
    x = [endpoints(:,i); 1];
    x = H2 * x;
    endpoints2(:,i) = x(1:2)/x(3);
end


% subplot(2,2,2)

hold on;
for i = 1:l
    x = [startpoints2(:,i) endpoints2(:,i)];
    plot(x(1,:),x(2,:))
end
hold off;

savefig('q1/h2.fig');
clf();

startpoints3 = zeros(2,l);
for i = 1:l
    x = [startpoints(:,i); 1];
    x = H3 * x;
    startpoints3(:,i) = x(1:2)/x(3);
end

endpoints3 = zeros(2,l);
for i = 1:l
    x = [endpoints(:,i); 1];
    x = H3 * x;
    endpoints3(:,i) = x(1:2)/x(3);
end


% subplot(2,2,3)

hold on;
for i = 1:l
    x = [startpoints3(:,i) endpoints3(:,i)];
    plot(x(1,:),x(2,:))
end
hold off;

savefig('q1/h3.fig');
clf();

startpoints4 = zeros(2,l);
for i = 1:l
    x = [startpoints(:,i); 1];
    x = H4 * x;
    startpoints4(:,i) = x(1:2)/x(3);
end

endpoints4 = zeros(2,l);
for i = 1:l
    x = [endpoints(:,i); 1];
    x = H4 * x;
    endpoints4(:,i) = x(1:2)/x(3);
end


% subplot(2,2,4)

hold on;
for i = 1:l
    x = [startpoints4(:,i) endpoints4(:,i)];
    plot(x(1,:),x(2,:))
end
hold off;

savefig('q1/h4.fig')

save('q1/transformed_endpts','startpoints1','startpoints2','startpoints3','startpoints4','endpoints1','endpoints2','endpoints3','endpoints4');