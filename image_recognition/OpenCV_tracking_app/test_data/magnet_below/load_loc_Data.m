clear; clc
data = load('NO_mag_kcf_locs.txt');
data2 = load('NO_mag_mil_locs.txt');
data3 = load('NO_mag_mdeidanflow_locs.txt');

locX = ((data(:,1) + 0.2*data(1,3))/500)*34- 16;
locX2 = ((data2(:,1) + 0.2*data2(1,3))/500)*34- 16;
locX3 = ((data3(:,1) + 0.2*data3(1,3))/500)*34- 16;

plot(locX)
hold on
plot(locX2)
hold on
% plot(locX3)
legend('kcf','mil','medianflow')