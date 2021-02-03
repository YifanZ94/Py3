clear; clc
data1 = load('LIS_30_mag.txt');
data2 = load('MMC_30_mag.txt');

data3 = load('30Env_mmc.txt');
data4 = load('30Per_mmc.txt');

data10 = load('LIS_30_env.txt');
data20 = load('MMC_30_env.txt');


x = 0:30;
%%
plot(x,data1(:,3)/100)
hold on
plot(x,data2(:,3))
hold on

xlabel('real distance(cm)')
ylabel('magnetic field(gauss)')
title('axis Z')
legend('LIS2MDL','MMC5603')

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
plot(x,-(data1(:,3) - data10(:,3))/100)
hold on
plot(x,data2(:,3)- data20(:,3))
hold on

xlabel('real distance(cm)')
ylabel('magnetic field(gauss)')
title('axis Z')
legend('LIS2MDL','MMC5603')

%%  env
plot(x,-(data4(:,3) - data3(:,3)))
hold on

xlabel('real distance(cm)')
ylabel('magnetic field(gauss)')
title('axis Z')
legend('MMC5603')

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