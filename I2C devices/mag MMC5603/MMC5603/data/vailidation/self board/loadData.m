clear; clc
data1 = load('LIS921data.txt');
data2 = load('MMCBoarddata.txt');
data3 = load('MMCS1data.txt');
data4 = load('MMCS2data.txt');
x = 1:30;
%%
plot(x,data1(:,3)/100)
hold on
plot(x,data2(:,3))
hold on
plot(x,data3(:,3))
hold on
plot(x,data4(:,3))
xlabel('real distance(cm)')
ylabel('magnetic field(gauss)')
title('axis Z')
legend('LIS2MDL','MMC5603','self-made 1','self-made 2')

%%
figure
plot(x,data1(:,1)/100)
hold on
plot(x,data2(:,2))
hold on
plot(x,data3(:,2))
hold on
plot(x,data4(:,2))
xlabel('real distance(cm)')
ylabel('magnetic field(gauss)')
title('axis X')
legend('LIS2MDL','MMC5603','self-made 1','self-made 2')

%%
figure
plot(x,data1(:,2)/100)
hold on
plot(x,data2(:,1))
hold on
plot(x,data3(:,1))
hold on
plot(x,data4(:,1))
xlabel('real distance(cm)')
ylabel('magnetic field(gauss)')
title('axis Y')
legend('LIS2MDL','MMC5603','self-made 1','self-made 2')

