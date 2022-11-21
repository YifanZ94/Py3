clear; clc
data = load('round3.mp4_locs.txt');

H_size = 500*(55/30);

locX = ((data(:,1) + 0.5*data(1,3))/500)*30 - 15;
locY = ((data(:,2) + 0.5*data(1,4))/H_size)*55;
locY = locY - locY(1);

subplot(121)
plot(locX)
subplot(122)
plot(locY)