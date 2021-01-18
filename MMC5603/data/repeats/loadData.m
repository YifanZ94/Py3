clear; clc
data1 = load('elec_50env.txt');
data10 = load('elec_50mag.txt');

std(data1(:,3))
std(data10(2:end,3))
mean(data1(2:end,3)-data10(2:end,3))

netZ = (data1(:,3) - data10(:,3));
x = 0:size(data1,1)-1;

%%  env
plot(x,data1(:,3))
title('power off')
xlabel('real distance(cm)')
ylabel('magnetic field(gauss)')
figure
plot(x,data10(:,3))
title('power on')
xlabel('real distance(cm)')
ylabel('magnetic field(gauss)')
figure
plot(x,data1(:,3),x,data10(:,3))
legend('power off','power on')
xlabel('real distance(cm)')
ylabel('magnetic field(gauss)')
