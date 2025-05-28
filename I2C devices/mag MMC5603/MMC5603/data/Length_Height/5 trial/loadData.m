clear; clc
H = [15,20,25];
T = [1,2,3,4,5];
F = [30,35,40];
des = zeros(3,3);
std = 0.003;

x1 = 0:10;
x2 = 10.1:0.1:20;
x3 = 21:30;

for i = 1:3
    figure
    for j = 1:5
        dataE = load(sprintf('MMC_H%d_F20_%d_mag.txt',H(i),T(j)));
        dataM = load(sprintf('MMC_H%d_F20_%d_env.txt',H(i),T(j)));
        dataM(2,:) = dataM(3,:);
        dataM(1,:) = dataM(3,:);
        dataE(1,:) = dataE(2,:);
        net = dataE(:,3) - dataM(:,3);
        plot(x1,net(1:11),x2,net(12:111),x3,net(112:end))
        hold on
        des(i,j) = find(net>0,1);
    end
end


