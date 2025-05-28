clear; clc
data1 = load('LIS2data.txt');
data2 = load('MMC2data.txt');
data3 = load('tYOST.txt');

data10 = load('LISenv2data.txt');
data20 = load('MMCenv2data.txt');
data30 = load('tenvYOST.txt');

simData = csvread('magline.csv',1,0);
x = 0:30;
%%
plot(x,data1(:,3)/100)
hold on
plot(x,data2(:,3))
hold on
plot(x,data3(:,2))
hold on
plot(x,simData(3000:-97:1,6)*10^5)
xlabel('real distance(cm)')
ylabel('magnetic field(gauss)')
title('axis Z')
legend('LIS2MDL','MMC5603','YOST IMU','simulation')

%%
figure
plot(x,data1(:,1)/100)
hold on
plot(x,data2(:,2))
hold on
plot(x,data3(:,1))
xlabel('real distance(cm)')
ylabel('magnetic field(gauss)')
title('axis X')
legend('LIS2MDL','MMC5603','YOST IMU')

%%
figure
plot(x,data1(:,2)/100)
hold on
plot(x,data2(:,1))
hold on
plot(x,data3(:,3))
xlabel('real distance(cm)')
ylabel('magnetic field(gauss)')
title('axis Y')
legend('MMC5603','YOST IMU')

%%  env
plot(x,(data1(:,3) - data10(:,3))/100)
hold on
plot(x,data2(:,3)-data20(:,3))
hold on
plot(x,data3(:,2)-data30(:,2))
hold on

xlabel('real distance(cm)')
ylabel('magnetic field(gauss)')
title('axis Z')
legend('LIS2MDL','MMC5603','YOST IMU')

%%
figure
plot(x,(data1(:,1)-data10(:,1))/100)
hold on
plot(x,data2(:,2)-data20(:,2))
hold on
plot(x,data3(:,1)-data30(:,1))
hold on 
% plot(x,simData(3000:-97:1,4)*10^3)
xlabel('real distance(cm)')
ylabel('magnetic field(gauss)')
title('axis X')
legend('LIS2MDL','MMC5603','YOST IMU')

% result with the most obvious deviation
%%
figure
plot(x,(data1(:,2)-data10(:,2))/100)
hold on
plot(x,(data2(:,1)-data20(:,1)))
hold on
plot(x,(data3(:,3)-data30(:,3)))
xlabel('real distance(cm)')
ylabel('magnetic field(gauss)')
title('axis Y')
legend('LIS2MDL','MMC5603','YOST IMU')