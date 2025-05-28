clear; clc
H = [15,25];
T = [1,2,3];
F = [30,35,40];

std = 0.003;

x1 = 0:13;
x2 = 13.1:0.1:23;
x3 = 24:36;

for i = 1:2
    figure
    for j = 1:3
        dataE = load(sprintf('MMC_H%d_F26_%d_mag.txt',H(i),T(j)));
        dataM = load(sprintf('MMC_H%d_F26_%d_env.txt',H(i),T(j)));
        dataM(1,:) = dataM(2,:);
        dataE(1,:) = dataE(2,:);
        net = dataE(:,3) - dataM(:,3);
        plot(x1,net(1:14),x2,net(15:114),x3,net(115:end))
        hold on
        des(i,j) = find(net>0,1);
    end
end
