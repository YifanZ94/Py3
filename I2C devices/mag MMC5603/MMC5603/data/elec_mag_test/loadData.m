clear; clc
data = load('elec_50P_1s.txt');

%%

mag = data(1:2:size(data,1)-1,:);
env = data(2:2:size(data,1),:);

x = 1:size(data,1)/2;

%%  plot
plot(x,env(:,3),x,mag(:,3))
legend('power off','power on')

ylable('Z (gauss)')
xlabel('test number')

